from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import pandas as pd

# 假设的数据集，包含一些示例数据
data = {
    '描述': ['描述1', '描述2', '描述3', '描述4'],
    '认证': ['是', '否', '否', '是'],
    'id': ['id1', 'id2', 'id3', 'id4'],
    'token': ['token1', 'token2', 'token3', 'token4'],
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
    '昵称': ['昵称1', '昵称2', '昵称3', '昵称4'],
    '属地': ['属地1', '属地2', '属地3', '属地4'],
    '评论文本': ['这是一条评论', '这也是一条评论', '还是一条评论', '评论'],
    '是否恶意用户': [0, 1, 0, 1]  # 目标变量
}

df = pd.DataFrame(data)

# 分离特征和目标变量
X = df.drop('是否恶意用户', axis=1)
y = df['是否恶意用户']

# 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 定义预处理转换器
text_features = ['描述', '认证', 'id', 'token', '昵称', '属地', '评论文本']
for col in text_features:
    X_train[col] = X_train[col].astype(str)
    X_test[col] = X_test[col].astype(str)

numeric_features = [col for col in X.columns if col not in text_features]

text_transformer = Pipeline(steps=[
    ('vect', TfidfVectorizer())
])

numeric_transformer = Pipeline(steps=[
    ('scale', StandardScaler())
])


# 使用ColumnTransformer来对不同类型的数据应用不同的处理
preprocessor = ColumnTransformer(
    transformers=[
        ('text', text_transformer, text_features),
        ('num', numeric_transformer, numeric_features)
    ])

# 创建管道
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

# 训练模型
pipeline.fit(X_train, y_train)

# 进行预测
y_pred = pipeline.predict(X_test)

# 评估模型
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))