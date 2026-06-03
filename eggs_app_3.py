iimport streamlit as st
import json

# ページの設定（スマホで見やすいようにワイドモードに設定）
st.set_page_config(page_title="エッグスンシングス会計シミュレーター（さいたま新都心店）", layout="centered")

st.title("🥞 Eggs 'n Things 会計シミュレーター")
st.caption("さいたま新都心店メニュー完全網羅（10%税込）")

# 2. メニューデータの完全定義（さいたま新都心店グランドメニュー＆最新キッズメニュー）
menu_data = {
    "1. パンケーキ": {
        "ストロベリー＆バナナ、ホイップクリームとマカダミアナッツ": 1749,
        "ストロベリー、ホイップクリームとマカダミアナッツ": 1683,
        "バナナ、ホイップクリームとマカダミアナッツ": 1683,
        "パイナップル、ホイップクリームとマカダミアナッツ": 1683,
        "ブルーベリー、ホイップクリームとマカダミアナッツ": 1749,
        "マンゴー、ホイップクリームとマカダミアナッツ": 1793,
        "ハワイファイブパンケーキ": 1925,
        "バナナ、ホイップクリームとマカダミアナッツ＋チョコレートソース": 1903,
        "チョコレートチップパンケーキ": 1287,
        "バターミルクパンケーキ": 1089,
    },
    "2. ワッフル": {
        "ワッフル（ストロベリー＆バナナ、ホイップクリーム）": 1749,
        "ワッフル（ストロベリー、ホイップクリーム）": 1683,
        "ワッフル（バナナ、ホイップクリーム）": 1683,
        "ワッフル（パイナップル、ホイップクリーム）": 1683,
        "ワッフル（ブルーベリー、ホイップクリーム）": 1749,
        "ワッフル（マンゴー、ホイップクリーム）": 1793,
        "ワッフル チョコレートチップ": 1287,
        "ワッフル バターミルク": 1089,
    },
    "3. クレープ＆フレンチトースト": {
        "レモン、サワークリーム クレープ": 1562,
        "ストロベリー、サワークリーム クレープ": 1661,
        "バナナ、サワークリーム クレープ": 1661,
        "カルアポークマヨネーズ＆チェダー クレープ": 1716,
        "スパム＆チェダー クレープ": 1661,
        "フルーツ・フレンチトースト": 1496,
        "コンプリート・フレンチトースト": 1529,
        "クラシック・フレンチトースト": 1298,
    },
    "4. エグスンベネディクト": {
        "ホウレン草とベーコン": 1639,
        "スパム ベネディクト": 1683,
        "スモークサーモンとアボカド": 1826,
        "BLT ベネディクト": 1826,
        "ホウレン草とカルアポーク": 1826,
        "ベジタリアン（ホウレン草・トマト・マッシュルーム）": 1639,
    },
    "5. オムレツ": {
        "スペシャルオムレツ（お肉全部入り）": 1705,
        "ホウレン草、ベーコンとチーズ": 1606,
        "ポテト、ベーコンとチーズ": 1606,
        "ポルトガルソーセージとチーズ": 1628,
        "ベジタリアン オムレツ": 1518,
    },
    "6. 肉料理＆卵料理": {
        "ビーフステーキ＆エッグス": 3619,
        "ポルトガルソーセージ＆エッグス": 1628,
        "ソーセージリンクス＆エッグス": 1606,
        "ベーコン＆エッグス": 1584,
        "スパム＆エッグス": 1584,
    },
    "7. ハワイアン＆大皿": {
        "ビッグアイランドプレート": 5478,
        "アイランドプレート": 4268,
        "サーフ＆ターフ (ステーキ＆ガーリックシュリンプ)": 4279,
        "テリヤキチキンプレート": 1606,
        "ガーリックシュリンプ ～ノースショアスタイル～": 2409,
        "モチコチキンプレート": 1639,
        "モチコチキン＆ワッフル": 1606,
        "ロコ・モコ": 1485,
        "アhiポケボウル": 1529,
        "スパイシーアhiポケボウル": 1529,
        "ハワイアンフライドライス": 1485,
        "グリルドチキン＆ガーリックライス": 1980,
        "タコライス": 1639,
    },
    "8. ハンバーガー": {
        "エグスンバーガー": 1716,
        "アボカドチーズバーガー": 1881,
        "カルアポークバーガー": 1650,
        "ヴィーガンアボカドバーガー": 1749,
    },
    "9. ププ・サラダ・アサイー": {
        "アhiポケ (単品)": 1089,
        "スパイシーアhiポケ (単品)": 1089,
        "カルアポーク＆キャベツ": 979,
        "モチコチキン (単品)": 1320,
        "ガーリックシュリンプ (単品)": 1760,
        "フライドポテト": 649,
        "スパムシーザーサラダ": 1529,
        "エグスンコブサラダ": 2189,
        "アサイーボウル ～フルーツ～": 1826,
        "アサイーボウル ～フルーツ＆チョコ～": 1826,
    },
    "10. キッズメニュー（小学生以下限定）": {
        "ケイキパンケーキ": 830,
        "ケイキロコモコ": 830,
        "ケイキテリヤキチキン": 830,
        "ケイキドリンク（アップル/オレンジ/ミルクなど）": 310,
    },
    "11. ドリンク：コーヒー＆ティー": {
        "100%コナコーヒー [Hot]": 968,
        "コナコーヒーブレンド [Hot]": 660,
        "アイスコーヒー": 660,
        "カフェラテ [Hot or Iced]": 770,
        "カプチーノ [Hot]": 770,
        "アールグレイティー [Hot or Iced]": 605,
        "プランテーションアイスティー": 660,
        "チョコレートドリンク [Hot or Iced]": 616,
        "ミルク [Hot or Iced]": 429,
    },
    "12. ドリンク：ハワイアン＆スカッシュ": {
        "ヴァージンマイタイ": 946,
        "ヴァージンブルーハワイ": 946,
        "ヴァージンピニャコラーダ": 1001,
        "ヴァージンラバフロー": 1089,
        "ジンジャーレモンスカッシュ": 770,
        "ベリー＆カシススカッシュ": 770,
        "ソルティライチスカッシュ": 770,
    },
    "13. ドリンク：フルーツ＆ヨーグルト・ソフト": {
        "ヨーグルトドリンク（バナナ）": 836,
        "ヨーグルトドリンク（ストロベリー）": 836,
        "ヨーグルトドリンク（マンゴー）": 836,
        "アサイーバナナヨーグルトドリンク": 979,
        "アサイーストロベリーヨーグルトドリンク": 979,
        "アサイーマンゴーヨーグルトドリンク": 979,
        "フルーツドリンク（オレンジ）": 616,
        "フルーツドリンク（グレープフルーツ）": 616,
        "フルーツドリンク（グァバ）": 616,
        "フルーツドリンク（パイナップル）": 616,
        "フルーツドリンク（マンゴー）": 616,
        "フルーツドリンク（クランベリー）": 616,
        "レモネード [Hot or Iced]": 616,
        "アイスティーレモネード": 616,
        "マンゴー＆パッションフルーツレモネード": 693,
        "コーラ / コーラ ゼロ": 616,
        "ジンジャーエール": 616,
        "トマトジュース": 616,
    },
    "14. トッピング・セット": {
        "ワイキキセットメニュー (1人分)": 2970,
        "追加ホイップクリーム": 550,
        "追加バニラアイス": 330,
        "トッピング（マカダミアナッツ/チョコ/フルーツなど）": 264,
    }
}

# --- 【修正：状態管理と初期化ロジックの改善】 ---
# URLパラメータから保存データをパースする
saved_order = {}
if "saved_data" in st.query_params:
    try:
        saved_order = json.loads(st.query_params["saved_data"])
    except:
        pass

saved_party_size = int(st.query_params.get("party_size", 2))

# st.session_state 側に値を一元化
if "party_size" not in st.session_state:
    st.session_state.party_size = saved_party_size

# 各メニューの数量をセッション状態にセット（入力用widgetの初期値に直結させる）
for category, items in menu_data.items():
    for item_name in items.keys():
        input_key = f"input_{item_name}"
        if input_key not in st.session_state:
            st.session_state[input_key] = saved_order.get(item_name, 0)

# --- 【修正②：リセット処理の完全化】 ---
def reset_all():
    # 各入力フォーム(widget)のセッション値をすべて直接0にする
    for category, items in menu_data.items():
        for item_name in items.keys():
            st.session_state[f"input_{item_name}"] = 0
    st.session_state.party_size = 2
    st.query_params.clear()

# 1. 人数選択
party_size = st.number_input(
    "お店に行く人数 (人)", 
    min_value=1, 
    max_value=20, 
    value=st.session_state.party_size, 
    step=1,
    key="party_size_input"
)
st.session_state.party_size = party_size

# リセットボタン
if st.button("🔄 選択をすべてリセットする", use_container_width=True, type="secondary"):
    reset_all()
    st.rerun()

total_price = 0
selected_items = []  # 内訳用リスト
current_order_to_save = {} # 保存用の現在の注文状態

# 3. UIの構築
st.write("### 📋 メメニューを選択")
for category, items in menu_data.items():
    with st.expander(category):
        for item_name, price in items.items():
            input_key = f"input_{item_name}"
            
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"**{item_name}**")
                st.caption(f"{price:,} 円")
            with col2:
                # valueではなく key を直接指定することで状態のズレを解消
                count = st.number_input(
                    "数量", 
                    min_value=0, 
                    max_value=20, 
                    key=input_key,
                    label_visibility="collapsed"
                )
            
            # 合計金額の計算
            total_price += price * count
            
            # 数量が1以上のものをカウント
            if count > 0:
                selected_items.append({
                    "name": item_name,
                    "count": count,
                    "subtotal": price * count
                })
                current_order_to_save[item_name] = count
                
            st.divider()

# --- 【修正①：変更のたびにリアルタイムでURLに同期保存】 ---
st.query_params["saved_data"] = json.dumps(current_order_to_save)
st.query_params["party_size"] = st.session_state.party_size


# 4. サイドバーの計算結果表示
st.sidebar.markdown("## 💰 計算結果")
st.sidebar.markdown(f"### **合計金額: {total_price:,} 円 (税込)**")

if party_size > 0:
    per_person = int(total_price / party_size)
    st.sidebar.markdown(f"### **1人あたり: {per_person:,} 円**")

st.sidebar.caption(f"※現在の設定人数: {party_size} 名")

# サイドバーの現在選択しているもの一覧
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛒 選択中のメニュー")
if selected_items:
    for item in selected_items:
        st.sidebar.markdown(f"**{item['name']}** x {item['count']}")
        st.sidebar.caption(f"小計: {item['subtotal']:,} 円")
else:
    st.sidebar.write("メニューが選択されていません")


# メイン画面の下部
st.write("---")
st.subheader("🛒 現在の選択合計")
st.metric(label="合計金額 (税込)", value=f"{total_price:,} 円")
st.metric(label="1人あたりの目安", value=f"{int(total_price / party_size):,} 円")

# メイン画面下部の現在選択しているもの一覧
st.write("#### 📋 選択中のメニュー内訳")
if selected_items:
    for item in selected_items:
        col_name, col_count, col_sub = st.columns([4, 1, 2])
        with col_name:
            st.write(item['name'])
        with col_count:
            st.write(f"x {item['count']}")
        with col_sub:
            st.write(f"{item['subtotal']:,} 円")
else:
    st.write("メニューが選択されていません")