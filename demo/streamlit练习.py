import streamlit as st

# 设置页面标题
st.set_page_config(page_title="蛊真人 - 短篇改编", page_icon="📚", layout="wide")

# 小说内容定义
novel_chapters = {
    "第一章：重生归来": """
    乌云密布，雷声滚滚。青茅山深处，一座破败的祠堂中，少年方源猛然睁开双眼。

    '我...竟然真的重生了？'方源感受着年轻的身体，前世五百年的记忆如潮水般涌来。

    上一世，他是名震天下的九转蛊仙，却在争夺春秋蝉时被群起而攻之，最终陨落。没想到上天垂怜，让他重回十六岁这年。

    '这一世，我定要夺回一切！'方源握紧拳头，眼中闪过决然之色。他清楚记得，三日后就是家族大比，那是他崛起的第一步。

    指尖轻抚过胸前的青铜戒指，那里藏着前世最重要的秘密——本命蛊的培育方法。
    """,

    "第二章：家族大比": """
    方家演武场，人声鼎沸。今日是三年一度的家族大比，族中子弟皆欲崭露头角。

    '方源，你不过炼体三重，也敢参加大比？'台下传来讥笑声。

    方源神色淡然：'成与不成，比过便知。'

    比试开始，对手是炼体五重的方正。众人皆以为方源必败，却不料战局突变。

    '爆血蛊！'方源低喝一声，气血瞬间暴涨，一拳轰出，竟将方正击退数步。

    这是他在坊市用全部积蓄换来的劣质蛊虫，虽只能使用一次，却足以改变战局。

    最终，方源以微弱优势取胜，获得进入藏经阁三天的资格。这才是他真正的目标。
    """,

    "第三章：藏经阁秘闻": """
    夜深人静，藏经阁内烛火摇曳。方源手持令牌，目光如炬。

    '前世我花了十年才找到的《百蛊真经》，今生却能提前获取。'方源翻阅古籍，嘴角微扬。

    突然，一道黑影闪过。'谁？'方源警觉转身。

    '小家伙，眼光不错。'黑袍老者浮现，'老夫观你有大机缘，可愿拜我为师？'

    方源心中一凛，这老者正是前世的启蒙恩师，但后来却...

    '弟子愿拜见师尊。'方源表面恭敬，暗自警惕。他知道，这位'师尊'将来会为夺他造化而下杀手。

    但此刻，他需要这份机缘来快速提升实力。
    """,

    "第四章：初遇红莲": """
    荒野之中，血腥味弥漫。方源循着气息来到一处战场遗迹。

    一具女尸静静躺在血泊中，面容安详，手中紧握一朵赤红莲花。

    '红莲？'方源瞳孔微缩。前世直到百年后才遇到的奇女子，今生竟提前出现。

    他蹲下身，发现女子还有微弱气息。'命蛊未散，尚有一线生机。'

    取出珍藏的续命蛊，小心翼翼种入女子体内。这是他仅剩的保命手段之一。

    '你救了我？'不知过了多久，女子缓缓睁眼，'为什么？'

    '因为你能帮我成仙。'方源直言不讳，'而且，你本就不该死在这里。'

    红莲怔住，随即展颜一笑：'有趣的小家伙。'
    """,

    "第五章：蛊虫之道": """
    深谷幽洞，方源盘膝而坐。面前摆放着数十只形态各异的蛊虫。

    '蛊之一道，取天地精华，纳万物生灵，铸就无上神通。'方源喃喃自语。

    手指轻点，一只碧绿小虫飞起，正是传说中的'养蛊虫'。它能加速其他蛊虫成长。

    '前世我耗费百年才培育出的完美蛊虫，今生有了它的帮助，或许十年便可达成。'

    突然，洞外传来脚步声。'方源师弟，原来你在这里。'是大师兄赵阳。

    方源袖中手指微动，养蛊虫悄然隐去。'见过师兄，我在修炼。'

    '师弟天赋异禀，进步神速啊。'赵阳意味深长，'不过修行之路漫长，还需脚踏实地。'

    方源心知肚明，这位'好心'的师兄，早已被长老收买，准备对他下手了。
    """
}

# 创建侧边栏用于章节选择
st.sidebar.title("📖 蛊真人")
selected_chapter = st.sidebar.radio(
    "选择章节阅读",
    list(novel_chapters.keys()),
    index=0
)

# 主页面内容
col1, col2 = st.columns([1, 4])

with col1:
    st.image("https://via.placeholder.com/150", caption="方源")

with col2:
    st.title("蛊真人")
    st.markdown("**作者：蛊真人** | 类别：玄幻修真**")

# 显示选中的章节内容
st.header(selected_chapter)
st.write(novel_chapters[selected_chapter])

# 添加分隔线
st.markdown("---")

# 底部信息
st.markdown("*第 {0} 章 / 共 {1} 章*".format(
    list(novel_chapters.keys()).index(selected_chapter) + 1,
    len(novel_chapters)
))

# 添加阅读进度提示
progress = (list(novel_chapters.keys()).index(selected_chapter) + 1) / len(novel_chapters)
st.progress(progress)

# 添加底部导航
col_prev, col_next = st.columns(2)

chapter_keys = list(novel_chapters.keys())
current_index = chapter_keys.index(selected_chapter)

with col_prev:
    if current_index > 0:
        prev_chapter = chapter_keys[current_index - 1]
        if st.button(f"⬅️ 上一章：{prev_chapter}"):
            selected_chapter = prev_chapter

with col_next:
    if current_index < len(chapter_keys) - 1:
        next_chapter = chapter_keys[current_index + 1]
        if st.button(f"下一章：{next_chapter} ➡️"):
            selected_chapter = next_chapter

# 添加版权说明
st.markdown("---")
st.caption("本作品为《蛊真人》同人创作，原作版权归原作者所有。")
