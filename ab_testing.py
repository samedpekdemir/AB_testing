import pandas as pd
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

df_c = pd.read_excel(r"C:\Users\Desktop\ödev_4\ab_testing.xlsx", sheet_name=0)
df_t = pd.read_excel(r"C:\Users\Desktop\ödev_4\ab_testing.xlsx", sheet_name=1)

# Facebook recently introduced what's called "maximumbidding".
# a new bidding type as an alternative to the bidding type Introduced "average bidding".
# One of our customers, bombabomba.com, is testing this new feature.
# The ultimate success criterion for Bombabomba.com is Purchase.
# Therefore, we refer to the Purchase metric for statistical testing should be focused.
# and A/B test will be done


# Impression: Number of advertisement view
# Click: Number of click viewed ads
# Purchase: Number of product through clicked ads
# Earning: Money earned after purchase

# There are two sheets as control group in which Maximum Bidding applied and
# test group in which Average Bidding applied in the excel file.




def check_pd(df):
    # function for descriptive statistic check to learn about data
    print(f"***\nhead\n{df.head()}\n*** ")
    print(f"***\nnull\n{df.isnull().sum()}\n*** ")
    print(f"***\ndescribe\n{df.describe().T}\n*** ")
    print(f"***\ndtypes\n{df.dtypes}\n*** ")
    print(f"***\nnunique\n{df.nunique()}\n*** ")


check_pd(df_c)
check_pd(df_t)
df_c
df_t

df_concat = pd.concat([df_c,df_t], ignore_index=True)
df_concat.head()

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.

############################
# 1. Set Hypothesis
############################

# H0: M1 = M2 there is no any signifcant difference between mean of control group and mean of test group
# H1: M1 != M2 ....there is....

############################
# 2. Assumption Check
############################

# normally distributed
# Variance Homogeneity

############################
# normally distributed assumption
############################

# H0: df_c["Purchase"] normally distributed.
# H1:..df_c["Purchase"] is not normally distributed.

# p-value < 0.05 HO rejected.
# p-value !<  0.05 H0 would not be rejected.

# shapiro for normal distribution check
test_stat, pvalue = shapiro(df_c["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# H0 would not be rejected because p-value is 0.5891 according to shapiro test

test_stat, pvalue = shapiro(df_t["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.1541 HO would not rejected

# So, they are normally distributed

############################
# Variance Homogenity Assumption
############################

# H0: Variances are homogeneous
# H1: Variances are not homogeneous

test_stat, pvalue = levene(df_c["Purchase"],
                           df_t["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.1083 > 0.05, so HO 'd not be rejected and they are homogeneous

# Two assumptions are satisfied,so parametric #ttest will be applied
# ttest tells us that if normally distributed and variance homogeneity assumptions are satisfied you can use me,
# and if normally distributed satisfied, but  variance homogeneity is dissatisfied you can use, but you have to
# set equal_var parameter as False


test_stat, pvalue = ttest_ind(df_c["Purchase"],
                           df_t["Purchase"],
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.3493 > 0.05, so their mean are not same Ho rejected
