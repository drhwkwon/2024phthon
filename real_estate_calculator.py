import streamlit as st
import math

# Streamlit 앱의 제목
st.title("주택 구매시 중개 수수료, 취득세, 대출 필요 금액 및 월 상환금 계산기")

# 주택 가격, 보유 자금, 이자율, 대출 기간 입력
price = st.number_input("주택 가격 (KRW)", min_value=0, step=1000000, format="%d")
own_money = st.number_input("보유 자금 (KRW)", min_value=0, step=1000000, format="%d")
interest_rate = st.number_input("대출 이자율 (%)", min_value=0.0, max_value=20.0, value=4.2, step=0.1, format="%.2f")
loan_term = st.number_input("대출 기간 (년)", min_value=1, max_value=30, value=20, step=1)

# 대출 필요 금액 계산 함수
def calculate_loan_amount(price, own_money):
    loan_amount = max(price - own_money, 0)  # 보유 자금이 충분하면 대출 금액을 0으로 설정
    return loan_amount

# 중개 수수료 계산 함수
def calculate_broker_fee(price):
    if price <= 500000000:
        fee_rate = 0.005
    elif price <= 900000000:
        fee_rate = 0.004
    elif price <= 1200000000:
        fee_rate = 0.005
    elif price <= 1500000000:
        fee_rate = 0.006
    else:
        fee_rate = 0.007
    return min(price * fee_rate, 25000000)  # 최대 2,500만 원 상한선

# 취득세 계산 함수
def calculate_acquisition_tax(price):
    if price <= 600000000:
        tax_rate = 0.01
    elif price <= 900000000:
        tax_rate = 0.02
    else:
        tax_rate = 0.03
    return price * tax_rate

# 월 상환금액 계산 함수 (원리금 균등 상환 방식)
def calculate_monthly_payment(loan_amount, interest_rate, loan_term):
    monthly_interest_rate = interest_rate / 100 / 12  # 월 이자율
    total_months = loan_term * 12  # 총 상환 개월 수
    if monthly_interest_rate == 0:
        return loan_amount / total_months  # 이자율이 0일 때
    else:
        monthly_payment = loan_amount * (monthly_interest_rate * math.pow(1 + monthly_interest_rate, total_months)) / (math.pow(1 + monthly_interest_rate, total_months) - 1)
        return monthly_payment

# 계산 버튼
if st.button("계산하기"):
    if price > 0:
        # 대출 필요 금액 계산
        loan_amount = calculate_loan_amount(price, own_money)

        # 중개 수수료와 취득세 계산
        broker_fee = calculate_broker_fee(price)
        acquisition_tax = calculate_acquisition_tax(price)

        # 월 상환금액 계산
        monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term)

        # 결과 출력
        st.write(f"**대출 필요 금액:** {loan_amount:,.0f} 원")
        st.write(f"**중개 수수료:** {broker_fee:,.0f} 원")
        st.write(f"**취득세:** {acquisition_tax:,.0f} 원")
        st.write(f"**총 비용:** {(broker_fee + acquisition_tax + price):,.0f} 원 (주택 가격 포함)")
        st.write(f"**월 상환금액 (원리금 균등 상환):** {monthly_payment:,.0f} 원")
    else:
        st.write("주택 가격을 입력해 주세요.")
