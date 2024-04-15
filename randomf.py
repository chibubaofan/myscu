# 导入必要的库
import jieba
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
# 假设的数据集，包含一些示例数据
data = {
    '评论文本': ['开车不能操作手机[呲牙][呲牙]有点意思', '这也是一条评论', '还是一条评论', '评论'],
    '描述': ['描述1', '描述2', '描述3', '描述4'],
    '认证': ['是', '否', '否', '是'],
    'id': ['id1', 'id2', 'id3', 'id4'],
    'token': ['token1', 'token2', 'token3', 'token4'],
    '昵称': ['昵称1', '昵称2', '昵称3', '昵称4'],
    '属地': ['属地1', '属地2', '属地3', '属地4'],
    '全部发布数': [100, 150, 200, 250],
    '原创发布数': [80, 120, 160, 200],
    '有互动的数量': [50, 75, 100, 125],
    '文章数量': [5, 10, 15, 20],
    '视频数量': [2, 4, 6, 8],
    '小视频数量': [1, 2, 3, 4],
    '微头条数量': [0, 1, 2, 3],
    '问答数量': [5, 5, 5, 5],
    '原创比例': [0.8, 0.8, 0.8, 0.8],
    '互动比例': [0.5, 0.5, 0.5, 0.5],
    'hot数量': [2, 4, 6, 8],
    'hot比例': [0.02, 0.026, 0.03, 0.032],
    '是否有合集': [1, 0, 1, 0],
    '点赞数': [1000, 1500, 2000, 2500],
    '粉丝数': [500, 1000, 1500, 2000],
    '关注数': [200, 300, 400, 500],
    '是否恶意用户': [0, 1, 0, 1]  # 目标变量
}
df = pd.DataFrame(data)
dfco=df.copy()
dfco['分词描述']=df['评论文本'].apply(jieba.lcut)
def tf_re(k):
    k='{}'.format(k)
    k=k.replace('[','').replace(']','')
    return k
dfco['分词描述']=dfco['分词描述'].apply(tf_re)
print(dfco)
from sklearn.feature_extraction.text import TfidfVectorizer

# 取出X和y
X = dfco['分词描述']
# 创建一个TfidfVectorizer的实例
vectorizer = TfidfVectorizer(stop_words='english',  # 这里的english可以换成停用词
                             use_idf=True,
                             smooth_idf=True)
# 使用Tfidf将文本转化为向量
X = vectorizer.fit_transform(X)
# 看看特征形状
X.shape
print(X)

#
#
#
#
# df = pd.DataFrame(data)
#
# # 分离特征和目标变量
# X = df.drop('是否恶意用户', axis=1)
# y = df['是否恶意用户']
#
# # 分割数据集为训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
#
# # 初始化随机森林模型
# # n_estimators表示要使用的树的数量
# # random_state参数确保结果的可重复性
# random_forest_model = RandomForestClassifier(n_estimators=100, random_state=42)
#
# # 训练模型
# random_forest_model.fit(X_train, y_train)
#
# # 预测测试集结果
# y_pred = random_forest_model.predict(X_test)
#
# # 计算并打印准确率
# accuracy = accuracy_score(y_test, y_pred)
# print(f'Accuracy: {accuracy}')

# 预测新数据（示例）
# 假设new_data是你想要预测的新数据，格式与X_train相同
# new_data = ...  # 这里应该是新数据的特征值
# new_prediction = random_forest_model.predict(new_data)
# print(f'New prediction: {new_prediction}')
