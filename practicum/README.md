# 🛠️ practicum

The **practicum** folder is dedicated to practical tasks on programming in Python and the "manual" implementation of machine learning methods in NumPy, followed by experiments for an in-depth understanding of algorithms.

---

## 📂 The structure of the practicum folder

- [0_python_practice/](0_python_practice/)
- Basic tasks for working with strings and collections (substring search, RLE compression, etc.)
- Operations with matrices: summation, shape change, and sparse representations  
  - Implementation and use of generators and iterators (batch generator, RLE iterator, etc.)  
  - Processing of an arbitrary number of arguments and polynomial calculations  

- [1_vectorization/](1_vectorization/)
- Acceleration of calculations by replacing loops with NumPy vector operations
- Vectorization of arithmetic on arrays and matrices  
  - Performance comparison "before" and "after" vectorization
- Analysis of bottlenecks in the code and optimization of work with data  

- [2_KNN/](2_KNN/)
- Implementation of the k-nearest neighbors algorithm "from scratch"  
  - Calculation of distances (Euclidean, Manhattan) and selection of the nearest points  
  - Selection of parameter k and normalization of features  
  - Quality assessment through cross-validation and visualization of results  

- [3_log_reg/](3_log_reg/)
- "From scratch": sigmoid function and logistic regression  
  - Gradient descent to optimize weights  
  - Training and validation on synthetic and real datasets  
  - Quality metrics: accuracy, ROC-AUC, consistency matrix analysis  

- [4_ensemble/](4_ensemble/)
- The simplest ensembles: bagging and random forest  
  - Gradient boosting of decision trees  
  - Combining predictions and voting (hard/soft voting)  
  - Study of the effect of the number of models and the depth of trees on accuracy  

---

## 🛠️ Technologies and tools

- **Language**: Python 3  
- **Libraries**:
- NumPy — "from scratch" implementation and vectorization
- Matplotlib / Seaborn  
- **Environment**: Jupyter Notebook / clean scripts `.py`  

---

**Each work includes a detailed theoretical justification, a Python implementation, and demonstration examples of the methods used.**
