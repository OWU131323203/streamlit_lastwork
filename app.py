# Streamlitアプリ：CoC_ranking.csvに基づいたシナリオランキング表示（見やすいレイアウト付き）
import streamlit as st
import pandas as pd
import plotly.express as px

# データ読み込み関数
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            st.error("データが空です。CSVファイルを確認してください。")
        return df
    except FileNotFoundError:
        st.error("CSVファイルが見つかりません。ファイルパスを確認してください。")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"データ読み込み中にエラーが発生しました: {e}")
        return pd.DataFrame()

# データ読み込み
df = load_data("data/CoC_ranking.csv")

if not df.empty:
    
    # タイトルと説明
    st.title("📚 TRPGのシナリオ集 -CoC編-")
    st.caption("クトゥルフ神話TRPGのシナリオを比較・分析し、紹介してくれるダッシュボードです。")
    st.markdown("---")

    # サイドバーでフィルタリング
    st.sidebar.header("🔍 フィルタ")
    st.sidebar.markdown("以下の条件でシナリオを絞り込むことができます。")

    tema = df['テーマ'].dropna().unique()
    selected_tema = st.sidebar.multiselect('テーマを選択', tema, default=tema[:2])

    tag1 = df['タグ1'].dropna().unique()
    selected_tag1 = st.sidebar.multiselect('タグ1を選択', tag1, default=tag1[:2])

    tag2 = df['タグ2'].dropna().unique()
    selected_tag2 = st.sidebar.multiselect('タグ2を選択', tag2, default=tag2[:2])

    tag3 = df['タグ3'].dropna().unique()
    selected_tag3 = st.sidebar.multiselect('タグ3を選択', tag3, default=tag3[:2])

    # フィルタリング処理
    def filter_data():
        return df[
            (df['テーマ'].isin(selected_tema)) &
            (
                (df['タグ1'].isin(selected_tag1)) |
                (df['タグ2'].isin(selected_tag2)) |
                (df['タグ3'].isin(selected_tag3))
            )
        ]

    filtered_df = filter_data()


    # タブで表示を切り替え
    tab1, tab2, tab3 = st.tabs(["🔍 検索結果一覧", "👑ランキング", "📊概要分析"])

    # タブ1: 検索結果一覧
    with tab1:

        st.markdown("### 🥰あなたの好きな傾向のシナリオ")

        if filtered_df.empty:
            st.warning("選択された条件に一致するデータがありません。")
        else:
            for idx, row in filtered_df.sort_values("テーマ別ランキング").head(50).iterrows():
                with st.container():
                    col1, col2 = st.columns([4, 1])

                    with col1:
                        st.subheader(f"# {row['シナリオ名']}")
                        st.write(f"**テーマ**: {row['テーマ']}")
                        st.write(f"**タグ**: {', '.join([str(row['タグ1']), str(row['タグ2']), str(row['タグ3'])])}")
                        st.write(f"[🔗 シナリオ詳細を見る]({row['URL']})")

                    with col2:
                        st.write(f"**テーマ別ランキング**: {row['テーマ別ランキング']}位")
                        st.write(f"**価格**: {row['販売価格']}")
                        st.write(f"**プレイ人数**: {row['プレイ人数']}")

                    st.markdown("---")

    # タブ2: ランキング
    with tab2:

        st.markdown("### 👑 テーマ別ランキング")

        tema_list = df['テーマ'].dropna().unique()
        selected_theme = st.selectbox("テーマを選択", tema_list)

        theme_df = df[df['テーマ'] == selected_theme]

        if theme_df.empty:
            st.warning("このテーマに該当するシナリオが見つかりませんでした。")
        else:
            ranked_df = theme_df.sort_values("テーマ別ランキング").head(20)

            for idx, row in ranked_df.iterrows():
                with st.container():
                    col1, col2 = st.columns([4, 2])

                    with col1:
                        st.subheader(f"#{int(row['テーマ別ランキング'])} - {row['シナリオ名']}")
                        st.write(f"**タグ**: {', '.join([str(row['タグ1']), str(row['タグ2']), str(row['タグ3'])])}")
                        st.write(f"**プレイ人数**: {row.get('プレイ人数', 'N/A')} | **価格**: {row.get('販売価格', 'N/A')}")
                        if pd.notna(row.get('URL')):
                            st.markdown(f"[🔗 シナリオ詳細を見る]({row['URL']})")

                    with col2:
                        st.write(f"**価格**: {row['販売価格']}")
                        st.write(f"**プレイ人数**: {row['プレイ人数']}")

                    st.markdown("---")

    # タブ3: 概要分析
    with tab3:
        st.markdown("### 📊 概要分析")
        
        # プレイ人数別のシナリオ数
        player_counts = df['プレイ人数'].value_counts().reset_index()
        player_counts.columns = ['プレイ人数', 'シナリオ数']
        fig4 = px.bar(player_counts, x='プレイ人数', y='シナリオ数', title='プレイ人数別シナリオ数')
        st.plotly_chart(fig4, use_container_width=True)
        #タグ1の分布（円グラフ）
        tag1_counts = df['タグ1'].value_counts()
        fig8 = px.pie(
            values=tag1_counts.values,
            names=tag1_counts.index,
            title="タグ1別シナリオ数分布"
        )
        st.plotly_chart(fig8, use_container_width=True)
        # タグ2の分布
        tag2_counts = df['タグ2'].value_counts().reset_index()
        tag2_counts.columns = ['タグ2', 'シナリオ数']
        fig6 = px.bar(tag2_counts, x='タグ2', y='シナリオ数', title='タグ2別シナリオ数')
        st.plotly_chart(fig6, use_container_width=True)
        # タグ3の分布
        tag3_counts = df['タグ3'].value_counts().reset_index()
        tag3_counts.columns = ['タグ3', 'シナリオ数']
        fig7 = px.bar(tag3_counts, x='タグ3', y='シナリオ数', title='タグ3別シナリオ数')
        st.plotly_chart(fig7, use_container_width=True)
        

        
