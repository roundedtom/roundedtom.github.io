import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats


class EventStudy(object):
    def __init__(
        self,
        sample,
        estimated_model,
        model_data,
        historical_returns,
        t1,
        t2,
        span,
        estimation_window_size,
    ):
        self.sample = sample
        self.estimated_model = estimated_model
        self.model_data = model_data
        self.historical_returns = historical_returns
        self.t1 = t1
        self.t2 = t2
        self.span = span
        self.estimation_window_size = estimation_window_size

    def get_event_date_index(self, ticker, event_date):
        historical_returns_of_ticker = self.historical_returns.query(
            "ticker == @ticker"
        ).reset_index(drop=True)

        historical_trading_days = historical_returns_of_ticker.loc[:, "TradingDate"]

        while 1:
            if event_date in historical_trading_days.values:
                event_date_index = list(historical_trading_days).index(event_date)
                break
            else:
                event_date = pd.to_datetime(
                    event_date, format="%Y-%m-%d"
                ) + pd.Timedelta(days=1)
                event_date = event_date.strftime("%Y-%m-%d")

        return historical_returns_of_ticker, historical_trading_days, event_date_index

    def get_window(self, ticker, event_date, market_type_id):
        (
            historical_returns_of_ticker,
            historical_trading_days,
            event_date_index,
        ) = self.get_event_date_index(ticker, event_date)

        # 判断估计期数据量大小，事件期数据量大小
        condition_estimation = (
            event_date_index - self.t1 - self.span
        ) >= self.estimation_window_size
        condition_event = (event_date_index + self.t2) < len(historical_trading_days)
        if all([condition_estimation, condition_event]):
            event_window = historical_returns_of_ticker.iloc[
                event_date_index + self.t1 : event_date_index + self.t2 + 1, :
            ]
            distance = self.span - self.t1
            estimation_window = historical_returns_of_ticker.iloc[
                event_date_index
                - distance
                - self.estimation_window_size : event_date_index - distance,
                :,
            ]
            event_window.insert(0, "MarketTypeID", market_type_id)
            estimation_window.insert(0, "MarketTypeID", market_type_id)
            return estimation_window, event_window
        else:
            return None

    def get_ticker_cars_with_famafrench_model(self, estimation_window, event_window):
        estimation_data = estimation_window.merge(
            self.model_data, how="left", on=["MarketTypeID", "TradingDate"]
        )
        event_data = event_window.merge(
            self.model_data, how="left", on=["MarketTypeID", "TradingDate"]
        )

        X = estimation_data.loc[:, ["RiskPremium", "SMB", "HML"]].values
        X = sm.add_constant(X)
        y = np.array(
            estimation_data.loc[:, "return"] - estimation_data.loc[:, "risk_free_rate"]
        ).reshape(-1, 1)
        model = sm.OLS(y, X)
        result = model.fit()

        normal_return = np.dot(
            sm.add_constant(
                event_data.loc[:, ["RiskPremium", "SMB", "HML"]].values,
                has_constant="add",
            ),
            result.params.reshape(-1, 1),
        ) + event_data.loc[:, "risk_free_rate"].values.reshape(-1, 1)

        abnormal_return = (
            event_data.loc[:, "return"].values.reshape(-1, 1) - normal_return
        )
        car = np.cumsum(abnormal_return, axis=0)
        return car.ravel()

    def get_ticker_cars_with_market_model(self, estimation_window, event_window):
        estimation_data = estimation_window.merge(
            self.model_data, how="left", on=["MarketTypeID", "TradingDate"]
        )
        event_data = event_window.merge(
            self.model_data, how="left", on=["MarketTypeID", "TradingDate"]
        )

        X = estimation_data.loc[:, ["market_returns"]].values
        X = sm.add_constant(X)
        y = np.array(estimation_data.loc[:, "return"]).reshape(-1, 1)
        model = sm.OLS(y, X)
        result = model.fit()

        normal_return = np.dot(
            sm.add_constant(
                event_data.loc[:, ["market_returns"]].values,
                has_constant="add",
            ),
            result.params.reshape(-1, 1),
        )

        abnormal_return = (
            event_data.loc[:, "return"].values.reshape(-1, 1) - normal_return
        )

        car = np.cumsum(abnormal_return, axis=0)

        return car.ravel()

    def get_sample_cars(self, progress):
        car_dict = {}
        event_with_insufficient_data = []
        TASKS_TO_BE_COMPLETED = len(self.sample)
        task_finished = 0
        if self.estimated_model == "FamaFrench":
            for ticker, event_date, market_type_id in zip(
                self.sample.loc[:, "ticker"],
                self.sample.loc[:, "EventDate"],
                self.sample.loc[:, "MarketTypeID"],
            ):
                try:
                    estimation_window, event_window = self.get_window(
                        ticker, event_date, market_type_id
                    )
                    car = self.get_ticker_cars_with_famafrench_model(
                        estimation_window, event_window
                    )
                    key = "&".join([ticker, event_date])
                    car_dict[key] = car
                except Exception:
                    # get_window return None
                    event_with_insufficient_data.append("&".join([ticker, event_date]))
                if progress:
                    task_finished += 1
                    print(
                        "\rTasks finished: {:^3.0f}%".format(
                            round(task_finished / TASKS_TO_BE_COMPLETED, 2) * 100
                        ),
                        end="",
                    )
        elif self.estimated_model == "Market":
            for ticker, event_date, market_type_id in zip(
                self.sample.loc[:, "ticker"],
                self.sample.loc[:, "EventDate"],
                self.sample.loc[:, "MarketTypeID"],
            ):
                try:
                    estimation_window, event_window = self.get_window(
                        ticker, event_date, market_type_id
                    )
                    car = self.get_ticker_cars_with_market_model(
                        estimation_window, event_window
                    )
                    key = "&".join([ticker, event_date])
                    car_dict[key] = car
                except Exception:
                    # logging.warning(e)
                    event_with_insufficient_data.append("&".join([ticker, event_date]))
                if progress:
                    task_finished += 1
                    print(
                        "\rTasks finished: {:^3.0f}%".format(
                            round(task_finished / TASKS_TO_BE_COMPLETED, 2) * 100
                        ),
                        end="",
                    )
        else:
            return None

        sample_cars_df = pd.DataFrame(car_dict, index=range(self.t1, self.t2 + 1))

        return sample_cars_df.T, event_with_insufficient_data

    def filter_ticker(self, ticker_event_date, event_with_insufficient_data):
        if ticker_event_date in event_with_insufficient_data:
            return False
        return True

    def get_result(self, progress=True):
        result = {}
        try:
            sample_cars_df, event_with_insufficient_data = self.get_sample_cars(progress)
        except Exception:
            print("请输入正确的正常收益率估计模型!可选 Market/FamaFrench")
            return None
        sample_remained = self.sample.loc[
            (
                self.sample.loc[:, "ticker"] + "&" + self.sample.loc[:, "EventDate"]
            ).apply(
                lambda ticker: self.filter_ticker(ticker, event_with_insufficient_data)
            ),
            :,
        ].reset_index(drop=True)

        test_result_dict = {}
        for col in sample_cars_df.columns:
            test_result = []
            res = stats.ttest_1samp(sample_cars_df.loc[:, col], 0)
            test_result.extend([res.statistic, res.pvalue])
            test_result_dict[col] = test_result
        t_p = pd.DataFrame(test_result_dict, index=["t-statstics", "p-value"]).T
        describe_result = pd.concat([sample_cars_df.describe().T, t_p], axis=1)

        result["describe_res"] = describe_result
        result["sample_removed"] = event_with_insufficient_data
        result["sample_remained"] = sample_remained
        result["sample_cars"] = sample_cars_df
        return result


def res_plot(sample_cars, confidence_interval=0.95):
    mean_series_of_cars = []
    lower_bounds_of_cars = []
    upper_bounds_of_cars = []
    for col in sample_cars.columns:
        cars_per_window = sample_cars.loc[:, col]
        mean_car = np.mean(cars_per_window)
        lower_bounds, upper_bounds = stats.t.interval(
            confidence=confidence_interval,
            df=len(cars_per_window) - 1,
            loc=mean_car,
            scale=stats.sem(cars_per_window),
        )
        mean_series_of_cars.append(mean_car)
        lower_bounds_of_cars.append(lower_bounds)
        upper_bounds_of_cars.append(upper_bounds)

    _, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    ax.set_xticks(
        list(sample_cars.columns),
        [str(c) for c in list(sample_cars.columns)],
    )
    ax.set_xlim([sample_cars.columns[0], sample_cars.columns[-1]])
    ax.plot(sample_cars.columns, [0] * len(sample_cars.columns), color="black")
    ax.plot(sample_cars.columns, mean_series_of_cars, color="blue", marker=".")
    ax.fill_between(
        sample_cars.columns,
        lower_bounds_of_cars,
        upper_bounds_of_cars,
        color="darkgrey",
        alpha=0.3,
    )
    plt.show()
    return None
