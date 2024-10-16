from fastapi import FastAPI, HTTPException
import pandas as pd
import json

# Crear la aplicación FastAPI
app = FastAPI()

# Cargar los DataFrames globalmente
df_games = pd.read_parquet("output_steam_games_limpio.parquet")
df_items = pd.read_parquet("australian_users_items_limpio.parquet")
df_reviews = pd.read_parquet("australian_user_reviews_limpio.parquet")
sentiment_copy = pd.read_parquet("user_reviews_analisis_ de_sentimientos.parquet")

# Copias para trabajar
df_games_copy = df_games.copy()
items_copy = df_items.copy()
reviews_copy = df_reviews.copy()

# Consulta 1: Developer
@app.get("/developer/{desarrollador}", name="developer")
async def developer(desarrollador: str):
    df_games_copy['release_date'] = pd.to_datetime(df_games_copy['release_date'], errors='coerce')
    developer_df = df_games_copy[df_games_copy['developer'] == desarrollador]

    items_por_año = developer_df.groupby(developer_df['release_date'].dt.year).size().reset_index(name='Cantidad de Items')
    gratis_por_año = developer_df[developer_df['price'] == 0].groupby(developer_df['release_date'].dt.year).size().reset_index(name='Contenido Free')

    resultado_df = items_por_año.merge(gratis_por_año, on='release_date', how='left').fillna(0)
    resultado_df['Contenido Free'] = (resultado_df['Contenido Free'] / resultado_df['Cantidad de Items'] * 100).astype(int).astype(str) + '%'
    resultado_df.rename(columns={'release_date': 'Año'}, inplace=True)

    return resultado_df.to_dict('records')

# Consulta 2: User Data
@app.get("/userdata/{user_id}", name="userdata")
async def userdata(user_id: str):
    items_copy['user_id'] = items_copy['user_id'].astype(str)
    reviews_copy['user_id'] = reviews_copy['user_id'].astype(str)

    user_items = items_copy[items_copy['user_id'] == user_id]
    df_games_copy['price'] = pd.to_numeric(df_games_copy['price'], errors='coerce')

    dinero = user_items.merge(df_games_copy[['id', 'price']], left_on='item_id', right_on='id')['price'].sum()
    total_items = user_items['items_count'].sum()

    user_reviews = reviews_copy[reviews_copy['user_id'] == user_id]
    porcentaje_recomendacion = (user_reviews['recommend'].sum() / user_reviews.shape[0]) * 100 if user_reviews.shape[0] > 0 else 0

    return {
        "Usuario": user_id,
        "Dinero gastado": f"{dinero:.2f} USD",
        "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
        "Cantidad de items": total_items
    }

# Consulta 3: User for Genre
@app.get("/UserForGenre/{genero}", name="UserForGenre")
async def UserForGenre(genero: str):
    juegos_genero = df_games_copy[df_games_copy['genres'] == genero]
    juegos_usuario = juegos_genero.merge(items_copy, left_on='id', right_on='item_id')

    horas_por_usuario = juegos_usuario.groupby('user_id')['playtime_forever'].sum().reset_index()
    if horas_por_usuario.empty:
        return {"Mensaje": f"No hay datos para el género '{genero}'."}

    usuario_max_horas = horas_por_usuario.loc[horas_por_usuario['playtime_forever'].idxmax()]['user_id']
    horas_por_año = juegos_usuario.groupby(juegos_usuario['release_date'].dt.year)['playtime_forever'].sum().reset_index()
    horas_por_año.rename(columns={'playtime_forever': 'Horas'}, inplace=True)

    return {
        f"Usuario con más horas jugadas para {genero}": usuario_max_horas,
        "Horas jugadas": horas_por_año.to_dict('records')
    }

# Consulta 4: Best Developer by Year
@app.get("/best_developer_year/{año}", name="best_developer_year")
async def best_developer_year(año: int):
    if año == -1:
        raise HTTPException(status_code=400, detail="El año ingresado es -1, lo cual no es válido.")

    df_fusionar = sentiment_copy.merge(df_games_copy[['id', 'developer']], left_on='item_id', right_on='id', how='left')
    df_fusionar['year_posted'] = df_fusionar['posted'].str.extract(r'(\b\d{4}\b)')
    df_fusionar.drop(columns=['posted'], inplace=True)

    df_año = df_fusionar[df_fusionar['year_posted'] == str(año)]
    df_filtrado = df_año[df_año['recommend'] & (df_año['sentiment_analysis'] == df_año['sentiment_analysis'].max())]

    top_developers = df_filtrado.groupby('developer')['recommend'].sum().sort_values(ascending=False).head(3)
    top_developers_dict = {f"Puesto {i+1}": dev for i, (dev, _) in enumerate(top_developers.items())}

    return top_developers_dict

# Consulta 5: Developer Reviews Analysis
@app.get("/developer_reviews_analysis/{desarrolladora}", name="developer_reviews_analysis")
async def developer_reviews_analysis(desarrolladora: str):
    merged_data = pd.merge(sentiment_copy, df_games_copy, left_on='item_id', right_on='id')
    filtered_data = merged_data[merged_data['sentiment_analysis'] != 1]
    grouped_data = filtered_data.groupby(['developer', 'sentiment_analysis']).size().unstack(fill_value=0)

    if desarrolladora in grouped_data.index:
        developer_reviews = grouped_data.loc[desarrolladora]
        developer_reviews_list = [{"Negativas": developer_reviews.get(0, 0)}, {"Positivas": developer_reviews.get(2, 0)}]
        return {desarrolladora: developer_reviews_list}
    else:
        raise HTTPException(status_code=404, detail=f"No se encontró información sobre la desarrolladora {desarrolladora}.")
