import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import io
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Animal

st.set_page_config(page_title="Classificação Taxonômica de Animais", layout="wide", page_icon="🦁")

init_db()

def get_initial_animal_data():
    dados_csv = {
        'Nome_Popular': [
            'Onça-Pintada', 'Elefante-Africano', 'Baleia-Jubarte', 'Águia-Americana', 
            'Cobra-Real', 'Abelha-Melífera', 'Polvo-Comum', 'Leão', 'Tigre', 'Leopardo',
            'Guepardo', 'Puma', 'Urso-Pardo', 'Urso-Polar', 'Lobo-Cinzento', 'Raposa-Vermelha',
            'Golfinho-Nariz-de-Garrafa', 'Orca', 'Cachalote', 'Tubarão-Branco', 'Tubarão-Martelo',
            'Arraia-Manta', 'Salmão-do-Atlântico', 'Atum-Rabilho', 'Cavalo-Marinho', 
            'Estrela-do-Mar', 'Camarão-Rosa', 'Lagosta-Americana', 'Caranguejo-Real',
            'Águia-Real', 'Falcão-Peregrino', 'Coruja-das-Torres', 'Papagaio-Cinzento',
            'Arara-Azul', 'Tucano-Toco', 'Beija-Flor-de-Topete', 'Pinguim-Imperador',
            'Avestruz', 'Ema', 'Crocodilo-do-Nilo', 'Jacaré-Americano', 'Iguana-Verde',
            'Camaleão-Velado', 'Dragão-de-Komodo', 'Píton-Reticulada', 'Anaconda-Verde',
            'Tartaruga-Marinha-Verde', 'Jabuti-Piranga', 'Rã-Touro', 'Salamandra-de-Fogo',
            'Formiga-Cortadeira', 'Borboleta-Monarca', 'Libélula-Azul', 'Grilo-Doméstico',
            'Louva-a-Deus', 'Besouro-Rinoceronte', 'Aranha-Teia-de-Funil', 'Tarântula-Mexicana',
            'Escorpião-Imperador'
        ],
        'Nome_Cientifico': [
            'Panthera onca', 'Loxodonta africana', 'Megaptera novaeangliae', 'Haliaeetus leucocephalus',
            'Ophiophagus hannah', 'Apis mellifera', 'Octopus vulgaris', 'Panthera leo', 'Panthera tigris',
            'Panthera pardus', 'Acinonyx jubatus', 'Puma concolor', 'Ursus arctos', 'Ursus maritimus',
            'Canis lupus', 'Vulpes vulpes', 'Tursiops truncatus', 'Orcinus orca', 'Physeter macrocephalus',
            'Carcharodon carcharias', 'Sphyrna mokarran', 'Mobula birostris', 'Salmo salar', 'Thunnus thynnus',
            'Hippocampus hippocampus', 'Asterias rubens', 'Farfantepenaeus duorarum', 'Homarus americanus',
            'Paralithodes camtschaticus', 'Aquila chrysaetos', 'Falco peregrinus', 'Tyto alba',
            'Psittacus erithacus', 'Anodorhynchus hyacinthinus', 'Ramphastos toco', 'Lophornis magnificus',
            'Aptenodytes forsteri', 'Struthio camelus', 'Rhea americana', 'Crocodylus niloticus',
            'Alligator mississippiensis', 'Iguana iguana', 'Chamaeleo calyptratus', 'Varanus komodoensis',
            'Malayopython reticulatus', 'Eunectes murinus', 'Chelonia mydas', 'Chelonoidis carbonarius',
            'Lithobates catesbeianus', 'Salamandra salamandra', 'Atta sexdens', 'Danaus plexippus',
            'Anax imperator', 'Acheta domesticus', 'Mantis religiosa', 'Oryctes nasicornis',
            'Atrax robustus', 'Brachypelma smithi', 'Pandinus imperator'
        ],
        'Reino': ['Animalia'] * 59,
        'Filo': [
            'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Arthropoda', 'Mollusca',
            'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata',
            'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata',
            'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Echinodermata', 'Arthropoda', 'Arthropoda',
            'Arthropoda', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata',
            'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata',
            'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata', 'Chordata',
            'Chordata', 'Arthropoda', 'Arthropoda', 'Arthropoda', 'Arthropoda', 'Arthropoda',
            'Arthropoda', 'Arthropoda', 'Arthropoda', 'Arthropoda'
        ],
        'Classe': [
            'Mammalia', 'Mammalia', 'Mammalia', 'Aves', 'Reptilia', 'Insecta', 'Cephalopoda',
            'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia',
            'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Mammalia', 'Chondrichthyes', 'Chondrichthyes',
            'Chondrichthyes', 'Actinopterygii', 'Actinopterygii', 'Actinopterygii', 'Asteroidea', 'Malacostraca', 'Malacostraca',
            'Malacostraca', 'Aves', 'Aves', 'Aves', 'Aves', 'Aves', 'Aves',
            'Aves', 'Aves', 'Aves', 'Aves', 'Reptilia', 'Reptilia', 'Reptilia',
            'Reptilia', 'Reptilia', 'Reptilia', 'Reptilia', 'Reptilia', 'Reptilia', 'Amphibia',
            'Amphibia', 'Insecta', 'Insecta', 'Insecta', 'Insecta', 'Insecta',
            'Insecta', 'Arachnida', 'Arachnida', 'Arachnida'
        ],
        'Ordem': [
            'Carnivora', 'Proboscidea', 'Cetacea', 'Accipitriformes', 'Squamata', 'Hymenoptera', 
            'Octopoda', 'Carnivora', 'Carnivora', 'Carnivora', 'Carnivora', 'Carnivora', 
            'Carnivora', 'Carnivora', 'Carnivora', 'Carnivora', 'Cetacea', 'Cetacea', 'Cetacea',
            'Lamniformes', 'Carcharhiniformes', 'Myliobatiformes', 'Salmoniformes', 'Perciformes',
            'Syngnathiformes', 'Valvatida', 'Decapoda', 'Decapoda', 'Decapoda', 'Accipitriformes',
            'Falconiformes', 'Strigiformes', 'Psittaciformes', 'Psittaciformes', 'Piciformes',
            'Apodiformes', 'Sphenisciformes', 'Struthioniformes', 'Rheiformes', 'Crocodilia',
            'Crocodilia', 'Squamata', 'Squamata', 'Squamata', 'Squamata', 'Squamata',
            'Testudines', 'Testudines', 'Anura', 'Urodela', 'Hymenoptera', 'Lepidoptera',
            'Odonata', 'Orthoptera', 'Mantodea', 'Coleoptera', 'Araneae', 'Araneae', 'Scorpiones'
        ],
        'Familia': [
            'Felidae', 'Elephantidae', 'Balaenopteridae', 'Accipitridae', 'Elapidae', 'Apidae',
            'Octopodidae', 'Felidae', 'Felidae', 'Felidae', 'Felidae', 'Felidae', 'Ursidae',
            'Ursidae', 'Canidae', 'Canidae', 'Delphinidae', 'Delphinidae', 'Physeteridae',
            'Lamnidae', 'Sphyrnidae', 'Mobulidae', 'Salmonidae', 'Scombridae', 'Syngnathidae',
            'Asteriidae', 'Penaeidae', 'Nephropidae', 'Lithodidae', 'Accipitridae', 'Falconidae',
            'Tytonidae', 'Psittacidae', 'Psittacidae', 'Ramphastidae', 'Trochilidae', 'Spheniscidae',
            'Struthionidae', 'Rheidae', 'Crocodylidae', 'Alligatoridae', 'Iguanidae', 'Chamaeleonidae',
            'Varanidae', 'Pythonidae', 'Boidae', 'Cheloniidae', 'Testudinidae', 'Ranidae',
            'Salamandridae', 'Formicidae', 'Nymphalidae', 'Aeshnidae', 'Gryllidae', 'Mantidae',
            'Scarabaeidae', 'Atracidae', 'Theraphosidae', 'Scorpionidae'
        ],
        'Genero': [
            'Panthera', 'Loxodonta', 'Megaptera', 'Haliaeetus', 'Ophiophagus', 'Apis', 'Octopus',
            'Panthera', 'Panthera', 'Panthera', 'Acinonyx', 'Puma', 'Ursus', 'Ursus', 'Canis',
            'Vulpes', 'Tursiops', 'Orcinus', 'Physeter', 'Carcharodon', 'Sphyrna', 'Mobula',
            'Salmo', 'Thunnus', 'Hippocampus', 'Asterias', 'Farfantepenaeus', 'Homarus',
            'Paralithodes', 'Aquila', 'Falco', 'Tyto', 'Psittacus', 'Anodorhynchus', 'Ramphastos',
            'Lophornis', 'Aptenodytes', 'Struthio', 'Rhea', 'Crocodylus', 'Alligator', 'Iguana',
            'Chamaeleo', 'Varanus', 'Malayopython', 'Eunectes', 'Chelonia', 'Chelonoidis',
            'Lithobates', 'Salamandra', 'Atta', 'Danaus', 'Anax', 'Acheta', 'Mantis', 'Oryctes',
            'Atrax', 'Brachypelma', 'Pandinus'
        ],
        'Especie': [
            'onca', 'africana', 'novaeangliae', 'leucocephalus', 'hannah', 'mellifera', 'vulgaris',
            'leo', 'tigris', 'pardus', 'jubatus', 'concolor', 'arctos', 'maritimus', 'lupus',
            'vulpes', 'truncatus', 'orca', 'macrocephalus', 'carcharias', 'mokarran', 'birostris',
            'salar', 'thynnus', 'hippocampus', 'rubens', 'duorarum', 'americanus', 'camtschaticus',
            'chrysaetos', 'peregrinus', 'alba', 'erithacus', 'hyacinthinus', 'toco', 'magnificus',
            'forsteri', 'camelus', 'americana', 'niloticus', 'mississippiensis', 'iguana',
            'calyptratus', 'komodoensis', 'reticulatus', 'murinus', 'mydas', 'carbonarius',
            'catesbeianus', 'salamandra', 'sexdens', 'plexippus', 'imperator', 'domesticus',
            'religiosa', 'nasicornis', 'robustus', 'smithi', 'imperator'
        ]
    }
    
    return pd.DataFrame(dados_csv)

def migrate_initial_data():
    db = SessionLocal()
    try:
        count = db.query(Animal).count()
        if count == 0:
            df = get_initial_animal_data()
            for _, row in df.iterrows():
                animal = Animal(
                    nome_popular=row['Nome_Popular'],
                    nome_cientifico=row['Nome_Cientifico'],
                    reino=row['Reino'],
                    filo=row['Filo'],
                    classe=row['Classe'],
                    ordem=row['Ordem'],
                    familia=row['Familia'],
                    genero=row['Genero'],
                    especie=row['Especie']
                )
                db.add(animal)
            db.commit()
    finally:
        db.close()

def load_animals_from_db():
    db = SessionLocal()
    try:
        animals = db.query(Animal).all()
        data = []
        for animal in animals:
            data.append({
                'Nome_Popular': animal.nome_popular,
                'Nome_Cientifico': animal.nome_cientifico,
                'Reino': animal.reino,
                'Filo': animal.filo,
                'Classe': animal.classe,
                'Ordem': animal.ordem,
                'Familia': animal.familia,
                'Genero': animal.genero,
                'Especie': animal.especie,
                'Conservation_Status': animal.conservation_status,
                'Image_URL': animal.image_url
            })
        return pd.DataFrame(data)
    finally:
        db.close()

migrate_initial_data()

st.title("🦁 Sistema de Classificação Taxonômica de Animais")
st.markdown("**Explore, analise e gerencie dados taxonômicos de forma interativa**")

df = load_animals_from_db()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dados Completos", 
    "🔍 Buscar e Filtrar", 
    "📈 Análise Estatística", 
    "📉 Visualizações", 
    "✅ Validação de Dados",
    "➕ Adicionar Animal"
])

with tab1:
    st.header("Base de Dados Completa")
    st.markdown(f"**Total de espécies catalogadas:** {len(df)}")
    
    st.dataframe(df, use_container_width=True, height=400)
    
    st.subheader("📥 Exportar Dados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Selecionar Colunas para Exportar:**")
        all_columns = df.columns.tolist()
        selected_columns = st.multiselect(
            "Colunas", 
            all_columns, 
            default=all_columns,
            key="export_columns"
        )
    
    if selected_columns:
        export_df = df[selected_columns]
        
        col_csv, col_json, col_excel = st.columns(3)
        
        with col_csv:
            csv = export_df.to_csv(index=False, encoding='utf-8')
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"classificacao_animais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        with col_json:
            json_str = export_df.to_json(orient='records', force_ascii=False, indent=2)
            st.download_button(
                label="⬇️ Download JSON",
                data=json_str,
                file_name=f"classificacao_animais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col_excel:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                export_df.to_excel(writer, index=False, sheet_name='Classificação')
            excel_data = output.getvalue()
            st.download_button(
                label="⬇️ Download Excel",
                data=excel_data,
                file_name=f"classificacao_animais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

with tab2:
    st.header("🔍 Buscar e Filtrar Animais")
    
    col1, col2 = st.columns(2)
    
    with col1:
        search_term = st.text_input(
            "Buscar por Nome Popular ou Científico:",
            placeholder="Digite o nome do animal..."
        )
    
    with col2:
        search_column = st.selectbox(
            "Buscar em:",
            ["Todos", "Nome_Popular", "Nome_Cientifico"]
        )
    
    st.subheader("Filtros por Taxonomia")
    
    filter_cols = st.columns(4)
    
    with filter_cols[0]:
        reino_filter = st.multiselect("Reino", df['Reino'].unique())
    
    with filter_cols[1]:
        filo_filter = st.multiselect("Filo", df['Filo'].unique())
    
    with filter_cols[2]:
        classe_filter = st.multiselect("Classe", df['Classe'].unique())
    
    with filter_cols[3]:
        ordem_filter = st.multiselect("Ordem", df['Ordem'].unique())
    
    filter_cols2 = st.columns(3)
    
    with filter_cols2[0]:
        familia_filter = st.multiselect("Família", df['Familia'].unique())
    
    with filter_cols2[1]:
        genero_filter = st.multiselect("Gênero", df['Genero'].unique())
    
    with filter_cols2[2]:
        especie_filter = st.multiselect("Espécie", df['Especie'].unique())
    
    filtered_df = df.copy()
    
    if search_term:
        if search_column == "Todos":
            filtered_df = filtered_df[
                filtered_df['Nome_Popular'].str.contains(search_term, case=False, na=False) |
                filtered_df['Nome_Cientifico'].str.contains(search_term, case=False, na=False)
            ]
        else:
            filtered_df = filtered_df[
                filtered_df[search_column].str.contains(search_term, case=False, na=False)
            ]
    
    if reino_filter:
        filtered_df = filtered_df[filtered_df['Reino'].isin(reino_filter)]
    if filo_filter:
        filtered_df = filtered_df[filtered_df['Filo'].isin(filo_filter)]
    if classe_filter:
        filtered_df = filtered_df[filtered_df['Classe'].isin(classe_filter)]
    if ordem_filter:
        filtered_df = filtered_df[filtered_df['Ordem'].isin(ordem_filter)]
    if familia_filter:
        filtered_df = filtered_df[filtered_df['Familia'].isin(familia_filter)]
    if genero_filter:
        filtered_df = filtered_df[filtered_df['Genero'].isin(genero_filter)]
    if especie_filter:
        filtered_df = filtered_df[filtered_df['Especie'].isin(especie_filter)]
    
    st.success(f"**{len(filtered_df)} animais encontrados**")
    st.dataframe(filtered_df, use_container_width=True, height=400)

with tab3:
    st.header("📈 Análise Estatística")
    
    st.subheader("Resumo Geral")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Espécies", len(df))
    
    with col2:
        st.metric("Total de Filos", df['Filo'].nunique())
    
    with col3:
        st.metric("Total de Classes", df['Classe'].nunique())
    
    with col4:
        st.metric("Total de Famílias", df['Familia'].nunique())
    
    st.divider()
    
    st.subheader("Distribuição por Níveis Taxonômicos")
    
    taxonomy_level = st.selectbox(
        "Selecione o Nível Taxonômico:",
        ["Filo", "Classe", "Ordem", "Familia", "Genero"]
    )
    
    distribution = df[taxonomy_level].value_counts().reset_index()
    distribution.columns = [taxonomy_level, 'Contagem']
    distribution['Percentual'] = (distribution['Contagem'] / len(df) * 100).round(2)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(distribution, use_container_width=True, height=400)
    
    with col2:
        st.metric("Grupos Únicos", len(distribution))
        st.metric("Mais Comum", distribution.iloc[0][taxonomy_level])
        st.metric("Contagem Máxima", distribution.iloc[0]['Contagem'])

with tab4:
    st.header("📉 Visualizações Interativas")
    
    viz_type = st.selectbox(
        "Tipo de Visualização:",
        ["Gráfico de Barras - Distribuição por Classe", 
         "Gráfico de Pizza - Distribuição por Filo",
         "Gráfico de Barras - Top 10 Famílias",
         "Gráfico de Barras Horizontais - Distribuição por Ordem",
         "Sunburst - Hierarquia Taxonômica"]
    )
    
    if viz_type == "Gráfico de Barras - Distribuição por Classe":
        classe_counts = df['Classe'].value_counts().reset_index()
        classe_counts.columns = ['Classe', 'Contagem']
        
        fig = px.bar(
            classe_counts, 
            x='Classe', 
            y='Contagem',
            title='Distribuição de Animais por Classe',
            labels={'Contagem': 'Número de Espécies'},
            color='Contagem',
            color_continuous_scale='viridis'
        )
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Gráfico de Pizza - Distribuição por Filo":
        filo_counts = df['Filo'].value_counts().reset_index()
        filo_counts.columns = ['Filo', 'Contagem']
        
        fig = px.pie(
            filo_counts, 
            values='Contagem', 
            names='Filo',
            title='Distribuição de Animais por Filo',
            hole=0.3
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Gráfico de Barras - Top 10 Famílias":
        familia_counts = df['Familia'].value_counts().head(10).reset_index()
        familia_counts.columns = ['Familia', 'Contagem']
        
        fig = px.bar(
            familia_counts, 
            x='Familia', 
            y='Contagem',
            title='Top 10 Famílias com Mais Espécies',
            labels={'Contagem': 'Número de Espécies'},
            color='Contagem',
            color_continuous_scale='blues'
        )
        fig.update_layout(xaxis_tickangle=-45, height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Gráfico de Barras Horizontais - Distribuição por Ordem":
        ordem_counts = df['Ordem'].value_counts().reset_index()
        ordem_counts.columns = ['Ordem', 'Contagem']
        
        fig = px.bar(
            ordem_counts, 
            y='Ordem', 
            x='Contagem',
            title='Distribuição de Animais por Ordem',
            labels={'Contagem': 'Número de Espécies'},
            orientation='h',
            color='Contagem',
            color_continuous_scale='sunset'
        )
        fig.update_layout(height=700)
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Sunburst - Hierarquia Taxonômica":
        fig = px.sunburst(
            df,
            path=['Filo', 'Classe', 'Ordem', 'Familia'],
            title='Hierarquia Taxonômica (Filo → Classe → Ordem → Família)',
            height=700
        )
        st.plotly_chart(fig, use_container_width=True)

with tab5:
    st.header("✅ Validação de Dados")
    
    st.subheader("Verificação de Integridade")
    
    missing_data = df.isnull().sum()
    duplicate_rows = df.duplicated().sum()
    duplicate_names = df['Nome_Popular'].duplicated().sum()
    duplicate_scientific = df['Nome_Cientifico'].duplicated().sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if missing_data.sum() == 0:
            st.success(f"✅ Sem Campos Vazios")
        else:
            st.error(f"❌ {missing_data.sum()} Campos Vazios")
    
    with col2:
        if duplicate_rows == 0:
            st.success(f"✅ Sem Linhas Duplicadas")
        else:
            st.warning(f"⚠️ {duplicate_rows} Linhas Duplicadas")
    
    with col3:
        if duplicate_names == 0:
            st.success(f"✅ Nomes Únicos")
        else:
            st.warning(f"⚠️ {duplicate_names} Nomes Repetidos")
    
    with col4:
        if duplicate_scientific == 0:
            st.success(f"✅ Nomes Científicos Únicos")
        else:
            st.warning(f"⚠️ {duplicate_scientific} Nomes Científicos Repetidos")
    
    st.divider()
    
    if missing_data.sum() > 0:
        st.subheader("Campos Vazios por Coluna")
        missing_df = pd.DataFrame({
            'Coluna': missing_data.index,
            'Valores Faltantes': missing_data.values
        })
        missing_df = missing_df[missing_df['Valores Faltantes'] > 0]
        st.dataframe(missing_df, use_container_width=True)
    
    if duplicate_rows > 0:
        st.subheader("Linhas Duplicadas")
        duplicated_df = df[df.duplicated(keep=False)]
        st.dataframe(duplicated_df, use_container_width=True)
    
    if duplicate_names > 0:
        st.subheader("Nomes Populares Duplicados")
        dup_names = df[df['Nome_Popular'].duplicated(keep=False)]
        st.dataframe(dup_names[['Nome_Popular', 'Nome_Cientifico', 'Classe']], use_container_width=True)
    
    if duplicate_scientific > 0:
        st.subheader("Nomes Científicos Duplicados")
        dup_sci = df[df['Nome_Cientifico'].duplicated(keep=False)]
        st.dataframe(dup_sci[['Nome_Popular', 'Nome_Cientifico', 'Classe']], use_container_width=True)
    
    st.divider()
    st.subheader("Verificação de Consistência Taxonômica")
    
    consistency_checks = []
    
    for col in ['Reino', 'Filo', 'Classe', 'Ordem', 'Familia', 'Genero', 'Especie']:
        empty_count = df[col].isna().sum()
        consistency_checks.append({
            'Nível': col,
            'Valores Únicos': df[col].nunique(),
            'Campos Vazios': empty_count,
            'Status': '✅ OK' if empty_count == 0 else '❌ Problema'
        })
    
    consistency_df = pd.DataFrame(consistency_checks)
    st.dataframe(consistency_df, use_container_width=True)
    
    st.divider()
    st.subheader("Validação de Hierarquias Taxonômicas")
    
    known_hierarchies = {
        'Chordata': ['Mammalia', 'Aves', 'Reptilia', 'Amphibia', 'Actinopterygii', 'Chondrichthyes'],
        'Arthropoda': ['Insecta', 'Arachnida', 'Malacostraca'],
        'Mollusca': ['Cephalopoda', 'Gastropoda', 'Bivalvia'],
        'Echinodermata': ['Asteroidea', 'Echinoidea', 'Holothuroidea']
    }
    
    hierarchy_issues = []
    
    for idx, row in df.iterrows():
        filo = row['Filo']
        classe = row['Classe']
        
        if filo in known_hierarchies:
            if classe not in known_hierarchies[filo]:
                hierarchy_issues.append({
                    'Animal': row['Nome_Popular'],
                    'Nome_Cientifico': row['Nome_Cientifico'],
                    'Filo': filo,
                    'Classe': classe,
                    'Problema': f'Classe "{classe}" não é típica do Filo "{filo}"'
                })
    
    scientific_name_issues = []
    for idx, row in df.iterrows():
        genero = row['Genero']
        especie = row['Especie']
        nome_cientifico = row['Nome_Cientifico']
        
        expected_name = f"{genero} {especie}"
        if nome_cientifico != expected_name:
            scientific_name_issues.append({
                'Animal': row['Nome_Popular'],
                'Nome_Cientifico_Atual': nome_cientifico,
                'Nome_Esperado': expected_name,
                'Problema': 'Nome científico não corresponde a Gênero + Espécie'
            })
    
    col1, col2 = st.columns(2)
    
    with col1:
        if len(hierarchy_issues) == 0:
            st.success(f"✅ Todas as hierarquias Filo-Classe estão consistentes ({len(df)} registros verificados)")
        else:
            st.warning(f"⚠️ {len(hierarchy_issues)} inconsistências de hierarquia encontradas")
    
    with col2:
        if len(scientific_name_issues) == 0:
            st.success(f"✅ Todos os nomes científicos estão consistentes com Gênero + Espécie")
        else:
            st.warning(f"⚠️ {len(scientific_name_issues)} nomes científicos inconsistentes")
    
    if hierarchy_issues:
        st.subheader("Problemas de Hierarquia Taxonômica")
        hierarchy_df = pd.DataFrame(hierarchy_issues)
        st.dataframe(hierarchy_df, use_container_width=True)
        st.info("💡 Verifique se a Classe está corretamente associada ao Filo para cada animal listado acima.")
    
    if scientific_name_issues:
        st.subheader("Inconsistências em Nomes Científicos")
        scientific_df = pd.DataFrame(scientific_name_issues)
        st.dataframe(scientific_df, use_container_width=True)
        st.info("💡 O nome científico deve ser composto por Gênero + Espécie (nomenclatura binomial).")

with tab6:
    st.header("➕ Adicionar Novo Animal")
    
    with st.form("add_animal_form"):
        st.subheader("Preencha os Dados Taxonômicos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome_popular = st.text_input("Nome Popular*", placeholder="Ex: Leão-Marinho")
            nome_cientifico = st.text_input("Nome Científico*", placeholder="Ex: Panthera leo")
            reino = st.text_input("Reino*", value="Animalia")
            filo = st.text_input("Filo*", placeholder="Ex: Chordata")
        
        with col2:
            classe = st.text_input("Classe*", placeholder="Ex: Mammalia")
            ordem = st.text_input("Ordem*", placeholder="Ex: Carnivora")
            familia = st.text_input("Família*", placeholder="Ex: Felidae")
            genero = st.text_input("Gênero*", placeholder="Ex: Panthera")
        
        especie = st.text_input("Espécie*", placeholder="Ex: leo")
        
        submitted = st.form_submit_button("➕ Adicionar Animal", type="primary")
        
        if submitted:
            errors = []
            
            if not nome_popular:
                errors.append("Nome Popular é obrigatório")
            if not nome_cientifico:
                errors.append("Nome Científico é obrigatório")
            if not reino:
                errors.append("Reino é obrigatório")
            if not filo:
                errors.append("Filo é obrigatório")
            if not classe:
                errors.append("Classe é obrigatória")
            if not ordem:
                errors.append("Ordem é obrigatória")
            if not familia:
                errors.append("Família é obrigatória")
            if not genero:
                errors.append("Gênero é obrigatório")
            if not especie:
                errors.append("Espécie é obrigatória")
            
            db = SessionLocal()
            try:
                if db.query(Animal).filter(Animal.nome_popular == nome_popular).first():
                    errors.append(f"Animal '{nome_popular}' já existe na base de dados")
                
                if db.query(Animal).filter(Animal.nome_cientifico == nome_cientifico).first():
                    errors.append(f"Nome científico '{nome_cientifico}' já existe na base de dados")
            finally:
                db.close()
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                db = SessionLocal()
                try:
                    new_animal = Animal(
                        nome_popular=nome_popular,
                        nome_cientifico=nome_cientifico,
                        reino=reino,
                        filo=filo,
                        classe=classe,
                        ordem=ordem,
                        familia=familia,
                        genero=genero,
                        especie=especie
                    )
                    db.add(new_animal)
                    db.commit()
                    st.success(f"✅ Animal '{nome_popular}' ({nome_cientifico}) adicionado com sucesso!")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    db.rollback()
                    st.error(f"❌ Erro ao adicionar animal: {str(e)}")
                finally:
                    db.close()
    
    st.divider()
    st.subheader("Animais Recentemente Adicionados")
    recent_df = load_animals_from_db()
    st.dataframe(recent_df.tail(10), use_container_width=True)

st.divider()
st.caption("🦁 Sistema de Classificação Taxonômica - Desenvolvido com Streamlit")
