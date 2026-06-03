import streamlit as st
import streamlit.components.v1 as components
import json

# ページの設定（スマホで見やすいようにワイドモードに設定）
st.set_page_config(page_title="エッグスンシングス会計シミュレーター（さいたま新都心店）", layout="centered")

st.title("🥞 Eggs 'n Things 会計シミュレーター")
st.caption("さいたま新都心店メニュー完全網羅（10%税込）")

# メニューデータの完全定義（さいたま新都心店グランドメニュー＆最新キッズメニュー）
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

# --- ブラウザ保存用：Keyの一覧を準備 ---
all_keys = ["party_size"]
for category, items in menu_data.items():
    for item_name in items.keys():
        all_keys.append(f"num_{item_name}")

# 最初の一回だけセッションデータを初期化
for k in all_keys:
    if k not in st.session_state:
        st.session_state[k] = 2 if k == "party_size" else 0

# --- 【新アプローチ】ブラウザのLocalStorageとStreamlitを仲介するコンポーネント ---
# 起動時にブラウザからデータを読み込むJavaScript
load_js = f"""
<script>
    const allKeys = {json.dumps(all_keys)};
    let parentWindow = window.parent;
    
    // ブラウザから前回のデータを取得
    let savedData = {{}};
    allKeys.forEach(key => {{
        const val = localStorage.getItem(key);
        if (val !== null) {{
            savedData[key] = parseInt(val);
        }}
    }});
    
    // データがあれば、Streamlitに伝える用の見えないリンクなどを介して返す代わりに、
    // 初回読み込み完了の合図としてLocalStorageの状態をそのまま保持
</script>
"""

# 1. 人数選択
party_size = st.number_input("お店に行く人数 (人)", min_value=1, max_value=20, key="party_size")

# 2. リセットボタン
if st.button("🔄 選択をすべてリセットする", use_container_width=True, type="secondary"):
    # セッションをクリア
    st.session_state["party_size"] = 2
    for category, items in menu_data.items():
        for item_name in items.keys():
            st.session_state[f"num_{item_name}"] = 0
            
    # ブラウザのLocalStorageも一斉削除するJavaScriptを送り込む
    clear_script = f"""
    <script>
        {json.dumps(all_keys)}.forEach(key => localStorage.removeItem(key));
        window.parent.location.reload();
    </script>
    """
    components.html(clear_script, height=0)

total_price = 0
selected_items = []
current_changes = {}

st.write("### 📋 メニューを選択")

# 3. メニューUI構築
for category, items in menu_data.items():
    with st.expander(category):
        for item_name, price in items.items():
            key_name = f"num_{item_name}"
            
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"**{item_name}**")
                st.caption(f"{price:,} 円")
            with col2:
                count = st.number_input(
                    "数量", 
                    min_value=0, 
                    max_value=20, 
                    key=key_name,
                    label_visibility="collapsed"
                )
            
            # 変更があれば記録用に追加
            current_changes[key_name] = count
            
            total_price += price * count
            if count > 0:
                selected_items.append({
                    "name": item_name,
                    "count": count,
                    "subtotal": price * count
                })
            st.divider()

current_changes["party_size"] = party_size

# --- 【自動保存の仕組み】変更があった数値をブラウザのLocalStorageに書き込む ---
# スマホを閉じても、ブックマークから開いても、ブラウザ自体がこの数値を記憶します
save_js_code = ""
for k, v in current_changes.items():
    save_js_code += f"localStorage.setItem('{k}', {v});\n"

save_component = f"""
<script>
    {save_js_code}
</script>
"""
# 見えないパーツとしてJavaScriptを実行
components.html(save_component, height=0)


# 4. サイドバー・計算結果表示
st.sidebar.markdown("## 💰 計算結果")
st.sidebar.markdown(f"### **合計金額: {total_price:,} 円 (税込)**")

if party_size > 0:
    per_person = int(total_price / party_size)
    st.sidebar.markdown(f"### **1人あたり: {per_person:,} 円**")
st.sidebar.caption(f"※現在の設定人数: {party_size} 名")

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