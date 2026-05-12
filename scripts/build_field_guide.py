#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "data" / "prompts.jsonl"
ANNOTATIONS = ROOT / "data" / "prompt_annotations.jsonl"
DOCS = ROOT / "docs"

USE_CASES = [
    {
        "id": "persona-clones",
        "name": "原图人格分身",
        "short": "保留原图主体，再生成 chibi / mini me / doodle 分身。",
        "formula": "保留原图身份与环境 -> 添加多个 mini/chibi 角色 -> 分配动作与表情 -> 加贴纸、手写字、白描边",
    },
    {
        "id": "brand-system",
        "name": "品牌视觉系统",
        "short": "把 logo、品牌色、字体、应用 mockup 组织成品牌手册式海报。",
        "formula": "品牌资产 -> 视觉规则 -> 色彩/字体层级 -> 应用 mockup -> 高级案例研究版式",
    },
    {
        "id": "ip-poster",
        "name": "IP/角色商业海报",
        "short": "把角色、名画或文化 IP 转译成商业海报、设定图或强风格图像。",
        "formula": "IP/角色主体 -> 忠实或反差改写 -> 构图/光线 -> 海报化排版 -> 输出比例",
    },
    {
        "id": "product-ad",
        "name": "产品广告视觉",
        "short": "为饮料、手机、美妆、服饰等产品生成广告主视觉。",
        "formula": "产品主体 -> 使用场景/人物关系 -> 强透视或棚拍构图 -> 材质细节 -> 广告文字",
    },
    {
        "id": "food-commerce",
        "name": "电商/食物摄影",
        "short": "生成食品、餐饮、ASMR 和消费场景的高质感图像。",
        "formula": "食物主体 -> 镜头视角 -> 光线/材质/热气 -> 食欲细节 -> 干净商业摄影",
    },
    {
        "id": "infographic",
        "name": "信息图/知识卡片",
        "short": "把知识、步骤、角色设定或技术说明组织成可读图像。",
        "formula": "主题 -> 信息层级 -> 网格/分区 -> 标签/图标/步骤 -> 清晰文字与参考表",
    },
    {
        "id": "video-storyboard",
        "name": "视频分镜/运动序列",
        "short": "用单图承载分镜、动作序列、视频首帧或短片流程。",
        "formula": "视频目标 -> 镜头/时间段 -> 动作连续性 -> 分格或首帧 -> 运动与声音提示",
    },
    {
        "id": "ui-mockup",
        "name": "UI / App Mockup",
        "short": "把网站、移动端、界面组件或数字产品场景纳入图像生成。",
        "formula": "产品/品牌 -> 屏幕或界面载体 -> UI 模块 -> CTA/层级 -> 真实设备或展示场景",
    },
    {
        "id": "meme-anti",
        "name": "梗图/反审美重绘",
        "short": "故意制造低质量、拙劣、反精致的 meme 传播效果。",
        "formula": "参考图轮廓 -> 故意低质量风格 -> 错位/笨拙/像素感 -> 保留可识别但不精确",
    },
]

GRAMMAR_MODULES = [
    {"id": "preservation", "name": "保留约束", "description": "身份、脸、姿势、光线、背景等不可破坏的编辑边界。"},
    {"id": "composition", "name": "构图", "description": "视角、镜头、留白、比例、分区、网格和画面重心。"},
    {"id": "lighting", "name": "光线", "description": "自然光、棚拍、电影光、轮廓光、阴影和高光。"},
    {"id": "color-system", "name": "色彩系统", "description": "品牌色、渐变、饱和度、HEX、冷暖关系和调色板。"},
    {"id": "typography-layout", "name": "文字/版式", "description": "标题层级、标签、说明文字、海报和信息图排版。"},
    {"id": "storyboard", "name": "分镜", "description": "时间段、场景、动作连续性、分格和视频流程。"},
    {"id": "negative-constraints", "name": "负面约束", "description": "no watermark、no artifacts、不要过度改动等排除规则。"},
    {"id": "style-transfer", "name": "风格转译", "description": "把主体转成 chibi、纸雕、漫画、赛博、反审美等视觉语言。"},
    {"id": "material-detail", "name": "材质细节", "description": "皮肤、头发、水滴、蒸汽、玻璃、纸张、包装和纹理。"},
]

CATEGORY_LABELS = {item["id"]: item["name"] for item in USE_CASES}

ANNOTATION_MAP = {
    "case-0001": ("ip-poster", [], ["composition", "lighting", "color-system", "typography-layout", "material-detail"], "Jinx 角色被转译成厚涂商业海报，重点控制侧脸构图、留白、低饱和色彩与电影光。", "角色忠实还原 -> 海报构图 -> 电影光/轮廓光 -> 色彩克制 -> 竖版商业排版"),
    "case-0002": ("food-commerce", ["video-storyboard"], ["composition", "lighting", "storyboard", "material-detail", "negative-constraints"], "用分秒场景描述食物 ASMR 画面，突出俯拍、蒸汽、蛋黄质感和微运动。", "食物场景 -> 俯拍镜头 -> 分段动作 -> 食欲细节 -> 干净无水印"),
    "case-0003": ("persona-clones", [], ["preservation", "style-transfer", "composition"], "保留健身照主体不变，在周围添加多个做不同动作的 chibi 分身。", "保留人物/背景 -> 生成 mini 分身 -> 每个分身有动作 -> 统一发型服装"),
    "case-0004": ("persona-clones", [], ["preservation", "style-transfer", "lighting", "typography-layout", "color-system"], "参考原脸和背景，叠加 3D chibi、白色 doodle 和手写贴纸文字。", "保留脸和背景 -> 添加 3D chibi -> doodle 装饰 -> 软 pastel 调色"),
    "case-0005": ("persona-clones", [], ["preservation", "style-transfer", "negative-constraints"], "用更强保留约束复制原图，再围绕主体生成健身主题 mini 角色。", "不改主体 -> 添加可爱分身 -> 分配健身动作 -> 保持原环境"),
    "case-0006": ("brand-system", ["ui-mockup"], ["composition", "color-system", "typography-layout", "material-detail"], "把 BTS logo 扩展成完整品牌系统海报，包含色板、字体、mockup 和图标。", "logo 输入 -> 品牌色系统 -> 字体层级 -> 多应用 mockup -> 机构级海报"),
    "case-0007": ("meme-anti", [], ["style-transfer", "composition"], "用反审美指令把参考图重绘成笨拙、像素化、鼠标涂鸦式 meme。", "参考图 -> 故意笨拙 -> MS Paint 质感 -> 似像非像"),
    "case-0008": ("ip-poster", [], ["style-transfer", "typography-layout", "composition"], "Naruto 被组织成 propaganda poster 的结构化 JSON prompt。", "IP 角色 -> 宣传画风格 -> 强标题/版式 -> 海报化输出"),
    "case-0009": ("infographic", ["ip-poster"], ["style-transfer", "typography-layout", "composition"], "把上传角色做成可爱的角色设计表，含表情、动作和小物件图标。", "参考角色 -> 大头像 -> 表情组 -> 动作姿态 -> 图标说明"),
    "case-0010": ("brand-system", ["food-commerce"], ["color-system", "typography-layout", "composition", "material-detail"], "Pizza Hut 品牌系统海报，强调从 logo 和品牌资产派生所有视觉元素。", "品牌 logo -> 品牌人格 -> 色彩字体 -> 食品气质 -> 系统化海报"),
    "case-0011": ("product-ad", [], ["composition", "lighting", "color-system", "material-detail", "typography-layout"], "西瓜汁罐的强透视广告人像，用低角度和产品前景制造商业冲击。", "产品前置 -> 人物辅助 -> 强透视 -> 夏日色彩 -> 商业摄影细节"),
    "case-0012": ("persona-clones", [], ["preservation", "style-transfer", "lighting", "color-system", "negative-constraints"], "小红书/Pinterest doodle 审美与 chibi 分身合并，强调不破坏原图色调。", "保留自然照片 -> doodle 装饰 -> chibi 分身 -> 少量手写字 -> 避免过度修图"),
    "case-0013": ("infographic", [], ["typography-layout", "composition", "color-system"], "把任意主题变成百科式教育信息图，强调收藏手册和社媒知识卡。", "主题 -> 百科参考页 -> 现代信息图 -> 分区层级 -> 可分享竖图"),
    "case-0014": ("infographic", [], ["composition", "typography-layout", "material-detail"], "冠状病毒缩放序列信息图，用多层尺度框架展示从微观到环境的层级。", "主题 -> 尺度层级 -> 圆形/六边形框 -> 微标签 -> 3D 科学渲染"),
    "case-0015": ("persona-clones", [], ["preservation", "style-transfer", "lighting", "typography-layout", "color-system"], "真实人脸参考加多姿态 3D chibi 与白色手绘装饰。", "真实脸 -> 同背景同光线 -> 多个 chibi -> 贴纸描边 -> 软萌韩系"),
    "case-0016": ("product-ad", ["ui-mockup"], ["composition", "typography-layout"], "面向 Facebook 广告批量生成素材，强调从网站信息和产品图片出发。", "产品/网站 -> 广告目标人群 -> 批量图像 -> 9:16 投放规格"),
    "case-0017": ("brand-system", ["product-ad"], ["color-system", "typography-layout", "composition", "material-detail"], "能量饮料品牌系统，覆盖 logo、品牌色、字体和真实包装 mockup。", "品牌名称 -> 人格关键词 -> 视觉系统 -> 包装/周边 mockup -> 案例研究"),
    "case-0018": ("persona-clones", [], ["preservation", "style-transfer"], "健身照片 mini 分身模板的变体，重点是保留主体并复制发型服装。", "保留照片 -> chibi 分身 -> 动作清单 -> 一致造型"),
    "case-0019": ("product-ad", [], ["composition", "typography-layout", "material-detail"], "NEXORA 鞋款社媒 campaign 海报，利用低角度和巨大标题制造冲击。", "产品广告 -> 低角度模特 -> 前景产品放大 -> 巨型标题 -> 功能图标"),
    "case-0020": ("ip-poster", ["infographic", "meme-anti"], ["typography-layout", "storyboard", "style-transfer"], "中文漫画长 prompt，测试多语言小字、画中画和复杂叙事一次生成。", "人物/IP 叙事 -> 漫画分镜 -> 多语言文字 -> 梗点反转 -> 一次生成"),
    "case-0021": ("product-ad", ["persona-clones"], ["preservation", "composition", "lighting", "material-detail"], "保留身份的 iPhone 风格创意人像，偏社交头像和产品感摄影。", "保留身份 -> 手机摄影视角 -> 真实环境 -> 清晰人物质感"),
    "case-0022": ("food-commerce", [], ["composition", "lighting", "material-detail"], "三文鱼牛油果吐司的高级编辑部食物摄影，强调自然窗光和浅景深。", "食物主体 -> 中性背景 -> 自然窗光 -> 浅景深 -> 高端编辑摄影"),
    "case-0023": ("ip-poster", [], ["composition", "lighting", "style-transfer", "material-detail"], "双重曝光编辑人像，以切片结构和纹理背景制造视觉实验感。", "人像主体 -> 双重曝光 -> 垂直切片 -> 高对比 -> 编辑部质感"),
    "case-0024": ("persona-clones", [], ["preservation", "style-transfer", "composition"], "高质量 chibi clone sticker diary，完整保留身份、姿势、光线和背景。", "上传照片 -> 全量保留 -> clone 贴纸日记 -> 分身互动"),
    "case-0025": ("ip-poster", [], ["composition", "lighting", "material-detail"], "同一个人与年轻自我相遇的分割时间肖像，用左右对齐表达叙事。", "同一人物 -> 垂直分割 -> 时间对照 -> 一致镜头 -> 情绪肖像"),
    "case-0026": ("meme-anti", ["ip-poster"], ["composition", "lighting", "style-transfer"], "让 AI 画出自己的日常偷拍照，用普通、瑕疵和偶然性反精致化。", "拟人主体 -> iPhone 偶然快照 -> 普通生活 -> 瑕疵感"),
    "case-0027": ("persona-clones", [], ["preservation", "style-transfer", "negative-constraints"], "分析上传图并严格保留主体结构，再添加手绘 doodle。", "分析原图 -> 保留主体构图光线 -> 添加 doodle -> 不改变身份比例"),
    "case-0028": ("food-commerce", [], ["composition", "lighting", "material-detail"], "台湾餐桌食物摄影，强调温暖自然光、丰富菜品和餐厅氛围。", "菜品组合 -> 餐桌场景 -> 暖光 -> 食材细节 -> 生活方式摄影"),
    "case-0029": ("persona-clones", [], ["style-transfer", "composition", "material-detail"], "Mini Me 世界，让多个动画小人和真实环境互动。", "真实照片 -> 迷你自己 -> 环境互动 -> 魔法日常感"),
    "case-0030": ("food-commerce", [], ["composition", "lighting", "material-detail"], "咖啡与冰淇淋的 cozy ad 食物摄影，突出倾倒瞬间和木桌氛围。", "饮品甜点 -> 近景动作 -> 暖色材质 -> 广告摄影"),
    "case-0031": ("ip-poster", ["persona-clones"], ["preservation", "lighting", "style-transfer", "material-detail"], "保留面部特征的未来蓝调知识分子人像，加赛博光效。", "保留脸 -> 未来棚拍 -> 蓝色光效 -> 电影质感"),
    "case-0032": ("ip-poster", [], ["preservation", "style-transfer", "material-detail"], "用参考人物生成树枝缠绕形成的人体艺术构图，测试材质转译。", "保留脸 -> 人体轮廓 -> 树枝材质 -> 超现实艺术构图"),
    "case-0033": ("food-commerce", ["video-storyboard"], ["composition", "lighting", "storyboard", "material-detail"], "拿铁在空中旋转，牛奶飞溅和咖啡颗粒构成动态产品图。", "饮品主体 -> 悬浮运动 -> 液体飞溅 -> 慢动作质感"),
    "case-0034": ("ip-poster", [], ["style-transfer", "composition", "color-system", "material-detail"], "宝可梦配色的 3D 纸雕 diorama，强调层叠纸切和超高饱和。", "IP 色彩 -> 纸雕场景 -> 层叠纵深 -> 高饱和细节"),
    "case-0035": ("ip-poster", [], ["composition", "lighting", "material-detail"], "透明亚克力方块中的小自我，利用物件隐喻制造心理叙事。", "人物 -> 透明容器 -> 内部小人 -> 反射光 -> 概念肖像"),
    "case-0036": ("ip-poster", ["video-storyboard"], ["preservation", "style-transfer", "composition", "material-detail"], "把上传人物放入高级纸雕弹出书幻想世界，偏世界观视觉设定。", "参考人物 -> 弹出书世界 -> 手工纸材质 -> 幻想叙事"),
    "case-0037": ("product-ad", [], ["composition", "typography-layout", "lighting", "material-detail"], "日本新酒 premium 海报，结合女性侍酒师、金色字体和奖章装饰。", "产品主题 -> 专家人物 -> 豪华字体 -> 奖章元素 -> 3:4 海报"),
    "case-0038": ("meme-anti", [], ["style-transfer", "composition"], "旧电脑绘图程序式笨拙重绘，与 case-0007 同属低质量梗图模板。", "参考图 -> 老式电脑画图 -> 鼠标涂鸦 -> 反精致"),
    "case-0039": ("ui-mockup", ["meme-anti"], ["typography-layout", "style-transfer"], "印度 Holi 主题二维码，展示复杂功能性图像的边界和失败风险。", "二维码目标 -> 节日主题 -> 功能扫描 -> 复杂度风险"),
    "case-0040": ("meme-anti", [], ["style-transfer", "composition", "typography-layout"], "低质量互联网 meme 风格的儿童涂鸦模板，可替换场景描述。", "meme 场景 -> 儿童涂鸦 -> MS Paint -> 低质量文字感"),
    "case-0041": ("infographic", [], ["typography-layout", "composition", "material-detail"], "单色 3D 女角色技术说明图，结合 instructional guide 与 diagram 布局。", "角色主体 -> 灰度渲染 -> 技术说明布局 -> 标签/网格"),
    "case-0042": ("infographic", [], ["typography-layout", "composition", "material-detail"], "4x4 网格角色参考表，强调单色、说明图和技术 diagram 美学。", "角色 -> 4x4 网格 -> 参考姿态 -> 技术标签"),
    "case-0043": ("infographic", ["video-storyboard"], ["typography-layout", "composition", "style-transfer"], "为 Seedance 视频准备角色 reference sheet，强调可复用的角色一致性。", "角色描述/参考图 -> reference sheet -> 表情/姿态 -> 视频一致性"),
    "case-0044": ("video-storyboard", ["infographic"], ["storyboard", "typography-layout", "composition"], "舞蹈动作序列说明表，把连续动作压缩成技术分格图。", "舞者主体 -> 动作步骤 -> 分格说明 -> 编舞参考"),
    "case-0045": ("video-storyboard", ["product-ad"], ["storyboard", "lighting", "composition", "material-detail"], "时尚变装 storyboard，用全球控制 prompt 生成电影化连续造型。", "时尚主题 -> 分镜结构 -> 造型变化 -> 电影光 -> 秀场广告"),
    "case-0046": ("product-ad", [], ["composition", "lighting", "typography-layout", "material-detail"], "Apple 风格智能手机广告海报，强调白棚、现代构图和全球 campaign 感。", "手机产品 -> 极简棚拍 -> 4:5 竖版 -> 广告标题 -> 高级材质"),
    "case-0047": ("food-commerce", ["video-storyboard"], ["storyboard", "lighting", "material-detail"], "韩式泡面广告分镜，包含时间、声音、慢动作蒸汽和配音。", "食品广告 -> 0-2 秒镜头 -> 声音/配音 -> 蒸汽细节 -> 短视频规格"),
    "case-0048": ("ip-poster", ["persona-clones"], ["preservation", "style-transfer", "composition"], "真实人物进入像素 RPG 世界，背景像素化而人物保持摄影真实。", "保留真人 -> 像素 RPG 背景 -> 真实/像素反差 -> 城市场景"),
    "case-0049": ("video-storyboard", ["ip-poster"], ["storyboard", "style-transfer", "composition"], "3x3 宫格奇幻战斗 storyboard，用同风格图继续编辑角色变化。", "角色动作 -> 3x3 分镜 -> 风格统一 -> 视频生成前置图"),
    "case-0050": ("ip-poster", ["food-commerce"], ["composition", "lighting", "style-transfer"], "台湾情侣旅行 12 图拼贴，强调手机随拍、情绪和地点记忆。", "旅行主题 -> 12 张拼贴 -> 手机快照 -> 情绪叙事"),
    "case-0051": ("infographic", [], ["typography-layout", "composition", "color-system"], "GET READY WITH ME 派对版步骤信息图，用 4x4 网格组织流程。", "主题流程 -> 16 步网格 -> 优雅字体 -> 柔和中性色"),
    "case-0052": ("ip-poster", ["video-storyboard"], ["style-transfer", "material-detail", "storyboard"], "3A RPG 角色概念图并衔接 Seedance 视频，展示图像到视频的生产链。", "角色概念 -> UE5/3A 风格 -> 参考图 -> 视频动作提示"),
    "case-0053": ("video-storyboard", ["ip-poster"], ["storyboard", "style-transfer", "composition"], "女性骑士变龙的 3x3 storyboard，直接服务后续视频生成。", "故事动作 -> 3x3 分镜 -> 转变节点 -> 视频生成提示"),
    "case-0054": ("product-ad", ["ip-poster"], ["composition", "typography-layout", "material-detail"], "足球球衣棚拍肖像，可替换 subject、队伍元素和号码。", "人物主体 -> 球衣产品 -> 队伍细节 -> 棚拍肖像 -> 数字/标识"),
    "case-0055": ("video-storyboard", ["infographic"], ["storyboard", "composition", "typography-layout"], "舞蹈序列说明表的变体，用专业技术 guide 表达动作连续性。", "舞者 -> 动作分解 -> 技术图表 -> 序列教学"),
    "case-0056": ("product-ad", [], ["composition", "lighting", "material-detail", "color-system"], "护肤品瓶身悬浮于爆裂水花中，典型高端产品摄影。", "产品瓶 -> 悬浮构图 -> 水花爆裂 -> 4:5 -> 高级商业摄影"),
    "case-0057": ("persona-clones", ["meme-anti"], ["preservation", "style-transfer", "typography-layout"], "中文打工人小人 prompt，在原图周围加 Q 版分身和吐槽手写字。", "保留办公室照 -> Q 版小人 -> 职场动作 -> 手写吐槽语"),
    "case-0058": ("ip-poster", ["infographic"], ["style-transfer", "typography-layout", "composition"], "日文世界观与原创角色设定资料，强调背景、建筑、服装、文化符号一致。", "世界观 -> 角色设定 -> 文化符号 -> 设定资料视觉"),
    "case-0059": ("ip-poster", [], ["composition", "lighting", "material-detail"], "雨中电影感男性特写肖像，突出水滴、湿发和情绪眼神。", "人物特写 -> 暴雨环境 -> 水滴材质 -> 情绪电影光"),
    "case-0060": ("product-ad", [], ["composition", "lighting", "material-detail", "color-system"], "Banana Glow 美妆管状产品，结合液体飞溅、种子和黄绿色渐变。", "产品包装 -> 水果汁液飞溅 -> 渐变背景 -> 光泽表面"),
    "case-0061": ("video-storyboard", ["infographic"], ["storyboard", "composition", "typography-layout"], "15 shot 女足比赛 storyboard，用 3x5 网格呈现从开始到结束的比赛流程。", "运动故事 -> 15 镜头 -> 3x5 网格 -> 连续比赛叙事"),
    "case-0062": ("meme-anti", ["ip-poster"], ["style-transfer", "typography-layout", "material-detail"], "蒙娜丽莎故障数字艺术，把古典油画与蓝屏、像素排序、加载图标碰撞。", "经典名画 -> glitch 效果 -> 数字错误符号 -> 古典/互联网反差"),
}


def load_prompts():
    return [json.loads(line) for line in PROMPTS.read_text(encoding="utf-8").splitlines() if line.strip()]


def clean_text(value):
    return " ".join(str(value).split())


def make_annotation(record):
    primary, secondary, tags, summary, formula = ANNOTATION_MAP[record["id"]]
    return {
        "id": record["id"],
        "primary_use_case": primary,
        "secondary_use_cases": secondary,
        "grammar_tags": tags,
        "summary_zh": summary,
        "formula_zh": formula,
        "featured": False,
        "featured_note": "",
    }


def write_annotations(records):
    existing = {}
    if ANNOTATIONS.exists():
        for line in ANNOTATIONS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                item = json.loads(line)
                existing[item["id"]] = item

    annotations = []
    for record in records:
        default = make_annotation(record)
        saved = existing.get(record["id"], {})
        annotations.append({**default, **saved})

    lines = [json.dumps(item, ensure_ascii=False) for item in annotations]
    ANNOTATIONS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return annotations


def build_cases(records, annotations):
    by_id = {item["id"]: item for item in annotations}
    cases = []
    for record in records:
        annotation = by_id[record["id"]]
        cases.append(
            {
                **annotation,
                "title": clean_text(record["title"]).replace("GPT Image 2 Prompt Case ", "Case "),
                "prompt": record["prompt"].strip(),
                "prompt_preview": clean_text(record["prompt"])[:260],
                "image": "./" + record["image"],
                "source_url": record["source_url"],
                "source_platform": record["source_platform"],
                "model": record["model"],
                "tweet_id": record["tweet_id"],
            }
        )
    return cases


def write_index():
    html = """<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>GPT Image 2 Viral Prompt Field Guide</title>
    <meta name="description" content="A curated use-case map for viral GPT Image 2 prompts." />
    <link rel="stylesheet" href="./styles.css" />
  </head>
  <body>
    <header class="site-header" id="top">
      <nav class="topbar" aria-label="Site navigation">
        <a class="brand" href="#top" aria-label="GPT Image 2 Viral Prompt Field Guide">
          <span class="brand-mark">G2</span>
          <span>GPT Image 2 Viral Prompt Field Guide</span>
        </a>
        <div class="topbar-meta" aria-label="Dataset summary">
          <span><strong id="caseCount">62</strong> cases</span>
          <span>9 families</span>
          <span>9 grammar modules</span>
        </div>
        <a class="source-link" href="../README.md">Source gallery</a>
      </nav>

      <section class="hero">
        <p class="eyebrow">GPT Image 2 Use-Case Map</p>
        <h1>这些爆款提示词，能拿来干什么？</h1>
        <p class="intro">
          先看用途，再看案例。这个 Field Guide 把 62 条互联网提示词整理成 9 类实际应用场景，方便创作者、设计师和增长团队快速找到可复用方向。
        </p>
      </section>
    </header>

    <main>
      <section class="section usecase-lead" aria-labelledby="usecaseTitle">
        <div class="section-heading">
          <p class="eyebrow">Use Cases</p>
          <h2 id="usecaseTitle">9 个用途族</h2>
          <p>这一层只回答一个问题：这些 GPT Image 2 prompt 到底可以被拿去做什么。</p>
        </div>
        <div class="usecase-grid" id="usecaseGrid"></div>
      </section>

      <section class="section case-panel" aria-labelledby="explorerTitle">
        <div class="panel-title">
          <p class="eyebrow">Case Explorer</p>
          <h2 id="explorerTitle">案例库</h2>
          <p>点击上方用途卡或在这里搜索，查看对应案例、摘要、公式和完整 prompt。</p>
        </div>

        <div class="filters" aria-label="Prompt filters">
          <label class="search-box">
            <span>搜索</span>
            <input id="searchInput" type="search" placeholder="输入 chibi、poster、食物、case-0006..." />
          </label>
          <div>
            <span class="filter-label">用途筛选</span>
            <div class="chip-row" id="usecaseFilters"></div>
          </div>
          <button class="ghost-button" id="clearFilters" type="button">Clear filters</button>
        </div>

        <div class="results-bar">
          <p id="resultCount"></p>
          <p id="activeFilters"></p>
        </div>
        <div class="case-grid" id="caseGrid"></div>
      </section>

      <section class="section grammar-section" aria-labelledby="grammarTitle">
        <div class="section-heading">
          <p class="eyebrow">Prompt Grammar</p>
          <h2 id="grammarTitle">语法控制层</h2>
          <p>用途之后，再看 prompt 是怎么控制图像的：保留、构图、光线、色彩、文字、分镜和材质。</p>
        </div>
        <div class="grammar-panel">
          <span class="filter-label">语法模块筛选</span>
          <div class="chip-row" id="grammarFilters"></div>
        </div>
      </section>

      <section class="section graph-appendix" aria-labelledby="graphTitle">
        <div class="section-heading">
          <p class="eyebrow">Graph Appendix</p>
          <h2 id="graphTitle">关系图附录</h2>
          <p>如果想看用途族和语法模块之间的连接，可以在这里查看。点击节点会同步筛选案例库。</p>
        </div>
        <div class="graph-panel">
          <div class="panel-header">
            <span>Use-case constellation</span>
            <button class="ghost-button" id="resetGraph" type="button">Reset</button>
          </div>
          <svg id="constellation" role="img" aria-label="Clickable prompt use-case graph"></svg>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>Images and prompts link back to their original public X/Twitter posts. This page is a research-oriented field guide built from the local gallery data.</p>
    </footer>

    <script src="./app.js"></script>
  </body>
</html>
"""
    (DOCS / "index.html").write_text(html, encoding="utf-8")


def write_styles():
    css = r""":root {
  --ink: #111827;
  --muted: #657083;
  --paper: #f6f8fb;
  --surface: #ffffff;
  --surface-soft: #eef4ff;
  --line: rgba(17, 24, 39, 0.1);
  --line-strong: rgba(17, 24, 39, 0.2);
  --accent: #2563eb;
  --accent-2: #0f9f8f;
  --accent-soft: rgba(37, 99, 235, 0.1);
  --shadow: 0 18px 50px rgba(31, 41, 55, 0.08);
  --radius: 24px;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  color: var(--ink);
  background:
    radial-gradient(circle at 15% 0%, rgba(37, 99, 235, 0.11), transparent 30rem),
    radial-gradient(circle at 90% 8%, rgba(15, 159, 143, 0.11), transparent 28rem),
    var(--paper);
  font-family: ui-sans-serif, "Avenir Next", "Noto Sans SC", "PingFang SC", sans-serif;
  overflow-x: hidden;
}

button, input { font: inherit; }

h1, h2, h3, p { margin-top: 0; }

.site-header {
  padding: 22px clamp(18px, 5vw, 72px) 34px;
}

.topbar,
.section,
.footer {
  max-width: 1440px;
  margin: 0 auto;
}

.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}

.brand, .source-link {
  color: inherit;
  text-decoration: none;
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.brand span:last-child {
  min-width: 0;
  overflow-wrap: anywhere;
}

.brand-mark {
  display: grid;
  width: 36px;
  height: 36px;
  place-items: center;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: white;
  font-size: 12px;
}

.topbar-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
  color: var(--muted);
  font-size: 12px;
  text-transform: uppercase;
}

.topbar-meta strong { color: var(--ink); }

.source-link,
.ghost-button {
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.68);
  color: var(--ink);
  cursor: pointer;
  font-size: 13px;
}

.source-link,
.ghost-button {
  padding: 9px 14px;
}

.hero {
  max-width: 920px;
  margin: clamp(56px, 9vw, 120px) auto 28px;
  text-align: center;
}

.eyebrow {
  margin: 0 0 12px;
  color: var(--accent);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.hero h1 {
  max-width: 900px;
  margin: 0 auto 18px;
  font-family: ui-serif, Georgia, "Times New Roman", "Noto Serif SC", "Songti SC", serif;
  font-size: clamp(42px, 7vw, 92px);
  letter-spacing: -0.06em;
  line-height: 1.02;
  overflow-wrap: anywhere;
}

.intro {
  max-width: 760px;
  margin: 0 auto;
  color: var(--muted);
  font-size: clamp(17px, 2vw, 22px);
  line-height: 1.7;
  overflow-wrap: anywhere;
}

.section {
  padding: 44px clamp(18px, 5vw, 72px);
}

.usecase-lead {
  padding-top: 12px;
}

.section-heading,
.panel-title {
  display: grid;
  grid-template-columns: minmax(220px, 0.34fr) minmax(0, 0.66fr);
  gap: 28px;
  align-items: end;
  margin-bottom: 24px;
}

.panel-title h2,
.section-heading h2 {
  margin: 0;
  font-family: ui-serif, Georgia, "Times New Roman", "Noto Serif SC", "Songti SC", serif;
  font-size: clamp(32px, 4.8vw, 64px);
  letter-spacing: -0.045em;
  line-height: 1.05;
}

.panel-title p:last-child,
.section-heading p:last-child {
  margin: 0;
  color: var(--muted);
  font-size: 17px;
  line-height: 1.7;
}

.usecase-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.usecase-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.84);
  box-shadow: var(--shadow);
  cursor: pointer;
  min-height: 265px;
  padding: 24px;
  transition: transform 0.18s ease, border-color 0.18s ease, background 0.18s ease;
}

.usecase-card:hover,
.usecase-card.active {
  border-color: var(--accent);
  background: linear-gradient(180deg, white, var(--surface-soft));
  transform: translateY(-3px);
}

.usecase-card .index {
  color: var(--accent);
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 12px;
  font-weight: 900;
}

.usecase-card h3 {
  margin: 20px 0 12px;
  font-size: 28px;
  letter-spacing: -0.04em;
}

.usecase-card p {
  margin-bottom: 18px;
  color: var(--muted);
  font-size: 16px;
  line-height: 1.65;
  overflow-wrap: anywhere;
}

.formula {
  border-top: 1px solid var(--line);
  padding-top: 16px;
  color: var(--ink);
  font-size: 14px;
  line-height: 1.6;
  overflow-wrap: anywhere;
}

.filters,
.grammar-panel {
  display: grid;
  gap: 14px;
  margin-bottom: 18px;
  border: 1px solid var(--line);
  border-radius: 22px;
  background: white;
  padding: 18px;
  box-shadow: var(--shadow);
}

.search-box {
  display: grid;
  gap: 8px;
  color: var(--ink);
  font-size: 13px;
  font-weight: 800;
}

.search-box input {
  width: 100%;
  border: 1px solid var(--line-strong);
  border-radius: 14px;
  background: #f9fbff;
  color: var(--ink);
  outline: none;
  padding: 13px 14px;
}

.filter-label {
  display: block;
  margin-bottom: 9px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  border: 1px solid var(--line);
  border-radius: 999px;
  background: #f9fbff;
  color: var(--ink);
  cursor: pointer;
  padding: 8px 12px;
  font-size: 13px;
  font-weight: 700;
}

.chip.active {
  border-color: var(--accent);
  background: var(--accent);
  color: white;
}

.results-bar {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 14px;
  margin: 20px 0;
  color: var(--muted);
  font-size: 14px;
}

.results-bar p { margin: 0; }
#activeFilters { color: var(--accent); font-weight: 800; }

.case-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.case-card {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  border: 1px solid var(--line);
  border-radius: 22px;
  background: white;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.thumb {
  position: relative;
  aspect-ratio: 4 / 3;
  background: #e5eaf2;
  overflow: hidden;
}

.thumb img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.badge {
  position: absolute;
  left: 12px;
  top: 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  color: var(--ink);
  padding: 6px 9px;
  font-size: 12px;
  font-weight: 850;
}

.badge-cross {
  left: auto;
  right: 12px;
  background: rgba(255, 255, 255, 0.82);
  color: var(--muted);
  font-weight: 700;
  font-size: 11px;
}

.case-card--cross {
  border-color: var(--line);
  opacity: 0.82;
}

.case-card--cross:hover {
  opacity: 1;
}

.secondary-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0 4px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.secondary-divider::before,
.secondary-divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: var(--line-strong);
}

.case-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 12px;
  padding: 18px;
}

.case-title {
  margin: 0;
  font-size: 15px;
  font-weight: 900;
}

.summary,
.preview {
  color: var(--muted);
  line-height: 1.6;
  overflow-wrap: anywhere;
}

.summary {
  margin-bottom: 0;
  font-size: 15px;
}

.preview {
  margin-bottom: 0;
  font-size: 13px;
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  border-radius: 999px;
  background: #eef2ff;
  color: #475569;
  padding: 5px 8px;
  font-size: 12px;
  font-weight: 800;
}

.case-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: auto;
  padding-top: 12px;
  border-top: 1px solid var(--line);
}

.case-actions a {
  color: var(--accent);
  font-size: 13px;
  font-weight: 900;
  text-decoration: none;
}

details {
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 10px 12px;
  background: #f9fbff;
}

summary {
  cursor: pointer;
  font-size: 13px;
  font-weight: 900;
}

pre {
  max-height: 340px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
  color: #273244;
  font-family: "SFMono-Regular", Consolas, monospace;
  font-size: 12px;
  line-height: 1.55;
}

.graph-panel {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: white;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--line);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

#constellation {
  display: block;
  width: 100%;
  height: 640px;
}

.graph-link { stroke: rgba(21, 19, 15, 0.15); stroke-width: 1; }
.graph-node { cursor: pointer; transition: opacity 0.2s ease; }
.graph-node:hover text { fill: var(--accent); }
.graph-node circle { stroke: rgba(21, 19, 15, 0.24); stroke-width: 1; }
.graph-node.active circle { stroke: var(--accent); stroke-width: 3; }
.graph-label {
  fill: var(--ink);
  font-family: ui-sans-serif, "Avenir Next", "Noto Sans SC", sans-serif;
  font-size: 13px;
  font-weight: 850;
  text-anchor: middle;
}
.graph-small { fill: var(--muted); font-size: 11px; font-weight: 750; }

.graph-appendix {
  padding-bottom: 26px;
}

.footer {
  padding: 26px clamp(18px, 5vw, 72px) 44px;
  color: var(--muted);
  font-size: 12px;
}

@media (max-width: 1280px) {
  .case-grid,
  .usecase-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 920px) {
  .section-heading,
  .panel-title {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .case-grid,
  .usecase-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .topbar {
    align-items: flex-start;
    flex-direction: column;
  }

  .brand {
    align-items: flex-start;
    width: 100%;
  }

  .source-link { display: none; }
  .hero {
    margin-top: 54px;
    text-align: left;
  }

  .hero h1 {
    max-width: 100%;
    font-size: clamp(36px, 12vw, 48px);
    letter-spacing: -0.045em;
    word-break: break-all;
  }

  .intro {
    margin-left: 0;
    margin-right: 0;
    font-size: 16px;
  }

  .case-grid, .usecase-grid { grid-template-columns: 1fr; }
  .results-bar { align-items: flex-start; flex-direction: column; }
  #constellation { height: 480px; }
}
"""
    (DOCS / "styles.css").write_text(css, encoding="utf-8")


def write_app(cases):
    payload = {
        "useCases": USE_CASES,
        "grammarModules": GRAMMAR_MODULES,
        "cases": cases,
    }
    data = json.dumps(payload, ensure_ascii=False)
    js = f"""const FIELD_GUIDE = {data};

const state = {{
  useCase: "all",
  grammar: "all",
  query: "",
}};

const byId = (id) => document.getElementById(id);
const useCaseById = new Map(FIELD_GUIDE.useCases.map((item) => [item.id, item]));
const grammarById = new Map(FIELD_GUIDE.grammarModules.map((item) => [item.id, item]));

function normalize(value) {{
  return String(value || "").toLowerCase();
}}

function setUseCase(id, shouldScroll = false) {{
  state.useCase = state.useCase === id ? "all" : id;
  renderAll();
  if (shouldScroll) {{
    byId("explorerTitle").scrollIntoView({{ behavior: "smooth", block: "start" }});
  }}
}}

function setGrammar(id) {{
  state.grammar = state.grammar === id ? "all" : id;
  renderAll();
}}

function clearFilters() {{
  state.useCase = "all";
  state.grammar = "all";
  state.query = "";
  byId("searchInput").value = "";
  renderAll();
}}

function matchesCase(item) {{
  const matchesUseCase =
    state.useCase === "all" ||
    item.primary_use_case === state.useCase ||
    item.secondary_use_cases.includes(state.useCase);
  const matchesGrammar =
    state.grammar === "all" || item.grammar_tags.includes(state.grammar);
  const haystack = normalize([
    item.id,
    item.title,
    item.prompt,
    item.summary_zh,
    item.formula_zh,
    useCaseById.get(item.primary_use_case)?.name,
    ...item.grammar_tags.map((tag) => grammarById.get(tag)?.name),
  ].join(" "));
  return matchesUseCase && matchesGrammar && haystack.includes(normalize(state.query));
}}

function sortedCases() {{
  const filtered = FIELD_GUIDE.cases.filter(matchesCase);
  if (state.useCase === "all") {{
    return filtered.sort((a, b) => Number(b.featured) - Number(a.featured) || a.id.localeCompare(b.id));
  }}
  // primary 案例排前，secondary（延伸参考）排后
  const primary = filtered.filter(item => item.primary_use_case === state.useCase);
  const secondary = filtered.filter(item => item.primary_use_case !== state.useCase);
  const sort = (a, b) => Number(b.featured) - Number(a.featured) || a.id.localeCompare(b.id);
  return [...primary.sort(sort), ...secondary.sort(sort)];
}}

function renderUseCases() {{
  byId("usecaseGrid").innerHTML = FIELD_GUIDE.useCases
    .map((item, index) => {{
      const count = FIELD_GUIDE.cases.filter(
        (caseItem) => caseItem.primary_use_case === item.id || caseItem.secondary_use_cases.includes(item.id)
      ).length;
      return `<article class="usecase-card ${{state.useCase === item.id ? "active" : ""}}" data-usecase="${{item.id}}" tabindex="0">
        <span class="index">${{String(index + 1).padStart(2, "0")}} / ${{count}} cases</span>
        <h3>${{item.name}}</h3>
        <p>${{item.short}}</p>
        <div class="formula">${{item.formula}}</div>
      </article>`;
    }})
    .join("");

  document.querySelectorAll(".usecase-card").forEach((card) => {{
    card.addEventListener("click", () => setUseCase(card.dataset.usecase, true));
    card.addEventListener("keydown", (event) => {{
      if (event.key === "Enter" || event.key === " ") setUseCase(card.dataset.usecase, true);
    }});
  }});
}}

function renderFilterChips() {{
  byId("usecaseFilters").innerHTML = [
    `<button class="chip ${{state.useCase === "all" ? "active" : ""}}" data-usecase-filter="all" type="button">全部用途</button>`,
    ...FIELD_GUIDE.useCases.map(
      (item) => `<button class="chip ${{state.useCase === item.id ? "active" : ""}}" data-usecase-filter="${{item.id}}" type="button">${{item.name}}</button>`
    ),
  ].join("");

  byId("grammarFilters").innerHTML = [
    `<button class="chip ${{state.grammar === "all" ? "active" : ""}}" data-grammar="all" type="button">全部语法</button>`,
    ...FIELD_GUIDE.grammarModules.map(
      (item) => `<button class="chip ${{state.grammar === item.id ? "active" : ""}}" data-grammar="${{item.id}}" type="button">${{item.name}}</button>`
    ),
  ].join("");

  document.querySelectorAll("[data-usecase-filter]").forEach((button) => {{
    button.addEventListener("click", () => {{
      state.useCase = button.dataset.usecaseFilter;
      renderAll();
    }});
  }});

  document.querySelectorAll("[data-grammar]").forEach((button) => {{
    button.addEventListener("click", () => {{
      state.grammar = button.dataset.grammar;
      renderAll();
    }});
  }});
}}

function renderCases() {{
  const cases = sortedCases();
  byId("resultCount").textContent = `Showing ${{cases.length}} of ${{FIELD_GUIDE.cases.length}} prompt cases`;
  const useLabel = state.useCase === "all" ? "全部用途" : useCaseById.get(state.useCase)?.name;
  const grammarLabel = state.grammar === "all" ? "全部语法" : grammarById.get(state.grammar)?.name;
  byId("activeFilters").textContent = `${{useLabel}} / ${{grammarLabel}}`;

  // 找出分隔点：primary 结束、secondary 开始的索引
  let dividerIndex = -1;
  if (state.useCase !== "all") {{
    dividerIndex = cases.findIndex(item => item.primary_use_case !== state.useCase);
  }}

  byId("caseGrid").innerHTML = cases
    .map((item, index) => {{
      const primary = useCaseById.get(item.primary_use_case);
      const isSecondary = state.useCase !== "all" && item.primary_use_case !== state.useCase;
      const tags = item.grammar_tags
        .map((tag) => `<span class="tag">${{grammarById.get(tag)?.name || tag}}</span>`)
        .join("");
      const badgeLabel = item.featured ? "Featured" : primary.name;
      const featured = `<span class="badge">${{badgeLabel}}</span>`;
      // 延伸参考标识：出现在右上角
      const crossBadge = isSecondary
        ? `<span class="badge badge-cross">延伸参考</span>`
        : "";
      // 分隔线：在第一个 secondary 案例前插入
      const divider = (index === dividerIndex)
        ? `<div class="secondary-divider" style="grid-column: 1 / -1;"><span>以下案例也适用于此场景，但主要归属其他用途</span></div>`
        : "";
      return divider + `<article class="case-card ${{isSecondary ? "case-card--cross" : ""}}">
        <div class="thumb">
          <img src="${{item.image}}" alt="${{escapeHtml(item.title)}}" loading="lazy" />
          ${{featured}}
          ${{crossBadge}}
        </div>
        <div class="case-body">
          <h3 class="case-title">${{item.id}} · ${{primary.name}}</h3>
          <p class="summary">${{item.summary_zh}}</p>
          <div class="formula">${{item.formula_zh}}</div>
          <div class="tag-row">${{tags}}</div>
          <p class="preview">${{escapeHtml(item.prompt_preview)}}...</p>
          <details>
            <summary>展开完整 prompt</summary>
            <pre>${{escapeHtml(item.prompt)}}</pre>
          </details>
          <div class="case-actions">
            <a href="${{item.source_url}}" target="_blank" rel="noreferrer">Original post</a>
            <span class="tag">${{item.model}}</span>
          </div>
        </div>
      </article>`;
    }})
    .join("");
}}

function escapeHtml(value) {{
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}}

function renderGraph() {{
  const svg = byId("constellation");
  const width = svg.clientWidth || 720;
  const height = svg.clientHeight || 570;
  const cx = width / 2;
  const cy = height / 2;
  const useRadius = Math.min(width, height) * 0.35;
  const grammarRadius = Math.min(width, height) * 0.19;
  svg.setAttribute("viewBox", `0 0 ${{width}} ${{height}}`);

  const useNodes = FIELD_GUIDE.useCases.map((item, index) => {{
    const angle = -Math.PI / 2 + (index / FIELD_GUIDE.useCases.length) * Math.PI * 2;
    return {{ ...item, type: "usecase", x: cx + Math.cos(angle) * useRadius, y: cy + Math.sin(angle) * useRadius }};
  }});
  const grammarNodes = FIELD_GUIDE.grammarModules.map((item, index) => {{
    const angle = -Math.PI / 2 + ((index + 0.5) / FIELD_GUIDE.grammarModules.length) * Math.PI * 2;
    return {{ ...item, type: "grammar", x: cx + Math.cos(angle) * grammarRadius, y: cy + Math.sin(angle) * grammarRadius }};
  }});

  const links = [];
  useNodes.forEach((useNode) => {{
    const relatedTags = new Set();
    FIELD_GUIDE.cases
      .filter((item) => item.primary_use_case === useNode.id || item.secondary_use_cases.includes(useNode.id))
      .forEach((item) => item.grammar_tags.forEach((tag) => relatedTags.add(tag)));
    grammarNodes
      .filter((grammarNode) => relatedTags.has(grammarNode.id))
      .forEach((grammarNode) => links.push([useNode, grammarNode]));
  }});

  svg.innerHTML = `
    <g>${{links
      .map(([a, b]) => `<line class="graph-link" x1="${{a.x}}" y1="${{a.y}}" x2="${{b.x}}" y2="${{b.y}}" />`)
      .join("")}}</g>
    <circle cx="${{cx}}" cy="${{cy}}" r="${{Math.max(54, grammarRadius * 0.32)}}" fill="rgba(23, 21, 18, 0.92)" />
    <text x="${{cx}}" y="${{cy - 5}}" fill="#f7f3ea" text-anchor="middle" font-family="ui-sans-serif, Avenir Next, sans-serif" font-size="13" font-weight="900">GPT Image 2</text>
    <text x="${{cx}}" y="${{cy + 14}}" fill="#d7cdbb" text-anchor="middle" font-family="ui-sans-serif, Avenir Next, sans-serif" font-size="11" font-weight="700">Prompt Atlas</text>
    <g>${{grammarNodes.map(renderGraphNode).join("")}}</g>
    <g>${{useNodes.map(renderGraphNode).join("")}}</g>
  `;

  svg.querySelectorAll(".graph-node").forEach((node) => {{
    node.addEventListener("click", () => {{
      if (node.dataset.type === "usecase") setUseCase(node.dataset.id);
      if (node.dataset.type === "grammar") setGrammar(node.dataset.id);
    }});
  }});
}}

function renderGraphNode(item) {{
  const active = item.type === "usecase" ? state.useCase === item.id : state.grammar === item.id;
  const radius = item.type === "usecase" ? 34 : 22;
  const fill = item.type === "usecase" ? "rgba(255, 252, 245, 0.95)" : "rgba(20, 92, 88, 0.1)";
  const labelClass = item.type === "usecase" ? "graph-label" : "graph-label graph-small";
  return `<g class="graph-node ${{active ? "active" : ""}}" data-type="${{item.type}}" data-id="${{item.id}}">
    <circle cx="${{item.x}}" cy="${{item.y}}" r="${{radius}}" fill="${{fill}}" />
    <text class="${{labelClass}}" x="${{item.x}}" y="${{item.y + radius + 18}}">${{item.name}}</text>
  </g>`;
}}

function renderAll() {{
  byId("caseCount").textContent = FIELD_GUIDE.cases.length;
  renderUseCases();
  renderFilterChips();
  renderCases();
  renderGraph();
}}

byId("searchInput").addEventListener("input", (event) => {{
  state.query = event.target.value;
  renderCases();
}});
byId("clearFilters").addEventListener("click", clearFilters);
byId("resetGraph").addEventListener("click", clearFilters);
window.addEventListener("resize", () => renderGraph());

renderAll();
"""
    (DOCS / "app.js").write_text(js, encoding="utf-8")


def main():
    records = load_prompts()
    missing = sorted(set(record["id"] for record in records) - set(ANNOTATION_MAP))
    if missing:
        raise SystemExit(f"Missing annotations: {', '.join(missing)}")
    DOCS.mkdir(exist_ok=True)
    annotations = write_annotations(records)
    write_app(build_cases(records, annotations))
    print(f"Wrote {ANNOTATIONS.relative_to(ROOT)}")
    print(f"Wrote {DOCS.relative_to(ROOT)}/app.js")


if __name__ == "__main__":
    main()
