import re
import streamlit as st
from collections import Counter

# 1. Contacts dictionary (Updated 889 to Yeshe Koh)
contacts = {
    "728": "Bryan", "199": "Sam Leong", "252": "Yvonne Tan", "710": "Eric Yip",
    "758": "Caren", "768": "Ken Goh", "778": "Tony", "788": "Teck Meng",
    "738": "Joey", "858": "Joe Yap", "668": "Rain Tan", "708": "Joanne Ng",
    "878": "Jingle", "141": "Shu Kee", "135": "Mimossa", "105": "Cynthia",
    "453": "Anto Hoong", "109": "Johnny", "19": "Lian Heok", "209": "Julie Chan",
    "729": "William Toh", "828": "Teo Zhen Wei", "918": "Huimei", "268": "Jojo Oo",
    "286": "Coco Chong", "599": "May Lou", "959": "Mei Ling", "255": "Lai Lean",
    "566": "Chun Huei", "779": "Chin Moi", "989": "Sex Leng", "955": "Yong Heng",
    "819": "Chun Yong", "648": "Yeong Chee", "829": "Mee Mee", "879": "Derek Yeo",
    "891": "Moi Heong", "876": "Jasmine Yien", "873": "Siew Lan", "839": "Xue Ru",
    "898": "Jacqueline", "863": "Bee Lan", "838": "Ai Ching", "889": "Yeshe Koh", # Updated name here
    "826": "Bee Suan", "813": "Danjuan", "836": "Poh Yoke", "872": "Siew Nee",
    "827": "Vera", "835": "Melly", "6": "Anicca Pte Ltd", "129": "Poh Hua",
    "399": "Betsy Fon", "166": "Su Mei", "413": "Yee Woon", "117": "Liang Ying",
    "198": "Qiao Ping", "18": "Shiqing", "144": "Lay Hua", "981": "DaQiang",
    "987": "Linqiong", "718": "Guo Ming", "306": "Chen Huang", "368": "Apple Huang",
    "727": "Jianrong", "789": "Xiyu", "181": "Liufang", "398": "Lifang",
    "798": "Chin Fan", "285": "Edwin Beh", "339": "JianFang", "666": "Chenfeng",
    "714": "Keh Sin", "871": "Yew Kin", "793": "Pei Chyi", "968": "Victor Chong",
    "688": "Chengrui", "333": "Wilson", "163": "Shanice", "222": "Steven Goh",
    "313": "Kenny Koh", "909": "Mac Lam", "979": "Yvonne Hui", "613": "Lina",
    "393": "Zhao Wei", "911": "Yew Pun", "939": "Teng Fong", "776": "Kar Yik",
    "933": "Jin Sin", "366": "Wei Shyang", "126": "Fai", "128": "Eric",
    "216": "Kelly Loo", "263": "Li Han", "621": "Wayne Ang", "249": "Gladys Tan",
    "155": "Joice Jedediah", "156": "Lisianah Soewarno", "737": "Henry Tay"
}

def parse_all_products(raw_text):
    # Find everything inside any bracket [...]
    brackets = re.findall(r"\[(.*?)\]", raw_text)
    if not brackets:
        return []

    product_counts = Counter()

    for content in brackets:
        # Skip brackets explicitly containing price metadata like SRF fees
        if "SRF" in content.upper():
            continue

        # Split items by comma if they are listed together
        items = [item.strip() for item in content.split(",") if item.strip()]

        for item in items:
            qty = 1
            product_name = item

            # Pattern A: "2 X NV LONGEVITY" or "2X NV..."
            match_front = re.match(r"^(\d+)\s*[xX]\s+(.+)$", item)
            # Pattern B: "NV LONGEVITY X2" or "NV... X 2"
            match_back = re.search(r"(.+?)\s*[xX]\s*(\d+)$", item)

            if match_front:
                qty = int(match_front.group(1))
                product_name = match_front.group(2).strip()
            elif match_back:
                qty = int(match_back.group(2))
                product_name = match_back.group(1).strip()
            
            # Pattern C: Check for complex tracking codes like "B-PS-E-07-328"
            # It extracts the product type acronym (e.g., 'PS' or 'RS') from the code block
            elif "-" in product_name:
                code_parts = product_name.split("-")
                if len(code_parts) >= 2:
                    # Usually picks the second item or matching token (e.g., PS, RS)
                    for part in code_parts:
                        if part.upper() in ["PS", "RS", "NV", "H"]: 
                            product_name = part.upper()
                            break
                    else:
                        product_name = code_parts[1].upper()

            # Handle explicit legacy single item short-codes (e.g., H523)
            m_h = re.search(r"H\d+", product_name)
            if m_h:
                product_name = m_h.group()

            product_counts[product_name] += qty

    # Format the product dictionary back to lines list
    output_lines = []
    for prod, count in product_counts.items():
        output_lines.append(f"✨ {count} x {prod}")
    
    return output_lines

# 3. Streamlit UI Elements
st.title("🏆 业绩捷报生成器")
st.write("输入包含编号和产品的原始文本，一键生成喜报。")

raw_input = st.text_input("在此粘贴输入内容:", placeholder="粘贴业绩文案...")

if st.button("生成捷报") or raw_input:
    if raw_input.strip():
        try:
            raw = raw_input.strip()
            code = raw.split("/")[0].strip()

            if code.isdigit():
                code = str(int(code))

            if code not in contacts:
                st.error("❌ 找不到对应的领导编号 (Code not found).")
            else:
                name = contacts[code]
                product_lines = parse_all_products(raw)

                if not product_lines:
                    st.warning("⚠️ 文本中未检测到有效的商品或明细信息。")
                else:
                    products_formatted = "\n".join(product_lines)

                    # Build message template
                    message = f"""让我们以最热烈的掌声，
恭喜今天下一位成功开单的优秀领导 👏✨

🔥 热烈恭喜 {name} 领导 🔥

成功带领团队签下：
{products_formatted}

气势已开，捷报先传！🚀

📈 六月目标：10M
让我们继续保持这股冲劲，
一起冲刺、一起突破、一起创下更高业绩！🔥🔥🔥"""

                    st.success("✅ 捷报生成成功！")
                    st.code(message, language="text")
                    
        except Exception as e:
            st.error(f"格式错误或解析失败: {e}")
            st.code(message, language="text")
                    
        except Exception as e:
            st.error(f"格式错误或解析失败: {e}")
