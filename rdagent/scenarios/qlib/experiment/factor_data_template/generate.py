import qlib

qlib.init(provider_uri="~/.qlib/qlib_data/cn_data")

from qlib.data import D

instruments = D.instruments()
fields = ["$open", "$close", "$high", "$low", "$volume", "$factor"]
# 数据源 /home/zxh/qlib_data 起始于 2020-01-02（仅 6 年历史，无 2008-2019 段）。
# 原 loc["2008-12-29":] 会导致 pandas 报 "not in index"（instruments 入池时间早于数据起点）。
# 改为 loc["2020-01-01":] 与数据实际范围对齐。
data = D.features(instruments, fields, freq="day").swaplevel().sort_index().loc["2020-01-01":].sort_index()

data.to_hdf("./daily_pv_all.h5", key="data")


fields = ["$open", "$close", "$high", "$low", "$volume", "$factor"]
# debug 段原为 2018-2019（数据集中不存在），改为 2024-2025（数据集最近的完整两年）。
data = (
    (
        D.features(instruments, fields, start_time="2024-01-01", end_time="2025-12-31", freq="day")
        .swaplevel()
        .sort_index()
    )
    .swaplevel()
    .loc[data.reset_index()["instrument"].unique()[:100]]
    .swaplevel()
    .sort_index()
)

data.to_hdf("./daily_pv_debug.h5", key="data")
