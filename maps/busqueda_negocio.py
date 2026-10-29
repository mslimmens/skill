import csv
from ddgs import DDGS

def buscar_negocios_web(query, region="ar-es", max_results=30):
    print(f"🔍 Buscando: '{query}' (Objetivo: {max_results} resultados)...\n")
    resultados_lista = []
    
    try:
        # Usamos backend="html" y pasamos max_results
        results = DDGS().text(query, region=region, max_results=max_results, backend="html")
        
        for r in results:
            titulo = r.get('title')
            link = r.get('href')
            descripcion = r.get('body')
            
            if not titulo or "DuckDuckGo" in titulo:
                continue
                
            print(f"📌 {titulo}")
            print(f"🔗 {link}")
            print(f"📝 {descripcion}\n" + "-"*50)
            
            resultados_lista.append({
                "Título": titulo,
                "Enlace": link,
                "Descripción": descripcion
            })
            
    except Exception as e:
        print(f"❌ Ocurrió un error durante la búsqueda: {e}")
        
    print(f"📊 Total de resultados obtenidos: {len(resultados_lista)}")
    return resultados_lista

def guardar_en_csv(datos, filename="negocios_encontrados.csv"):
    if not datos:
        print("⚠️ No hay datos para guardar.")
        return
    
    keys = datos[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(datos)
        
    print(f"💾 ¡Listo! Resultados guardados exitosamente en: '{filename}'")

if __name__ == "__main__":
    query_busqueda = "Ferreterías en Malvinas Argentinas, Buenos Aires"
    
    datos_encontrados = buscar_negocios_web(query_busqueda, max_results=30)
    guardar_en_csv(datos_encontrados)