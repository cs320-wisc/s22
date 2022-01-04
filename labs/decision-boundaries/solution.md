# Solution

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("poly", PolynomialFeatures(3)),
    ("std", StandardScaler()),
    ("lr", LogisticRegression()),
])
pipe.fit(df[["x", "y"]], df["z"])
df.plot.scatter(x="x", y="y", c=df["z"], vmin=-1)
x, y = np.meshgrid(np.arange(-3, 3, 0.01),
                   np.arange(ax.get_ylim()[0], ax.get_ylim()[1], 0.01))
predict_df = pd.DataFrame({
    "x": x.reshape(-1),
    "y": y.reshape(-1),
})
z = pipe.predict(predict_df).reshape(x.shape)
plt.contourf(x, y, z, alpha=0.1, cmap="binary")
```