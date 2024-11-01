import streamlit as st
import inflect

# 숫자를 한글로 변환하는 함수
def number_to_korean(n):
    units = ["", "만", "억", "조", "경"]
    nums = ["", "일", "이", "삼", "사", "오", "육", "칠", "팔", "구"]
    result = []
    unit_count = 0

    while n > 0:
        n, remainder = divmod(n, 10000)
        if remainder > 0:
            result.append(units[unit_count])
            result.append(str(remainder))
        unit_count += 1

    return ''.join(result[::-1])

# Streamlit 앱의 제목
st.title("주택 구매 비용 및 대출 상환금 계산기")

# 주택 가격 입력
price = st.number_input("주택 가격 (원)", min_value=0, step=1000000, format="%d")
st.write(f"입력한 주택 가격: {price:,}원 ({number_to_korean(price)} 원)")

# 보유 자금 입력
own_money = st.number_input("보유 자금 (원)", min_value=0, step=1000000, format="%d")
st.write(f"입력한 보유 자금: {own_money:,}원 ({number_to_korean(own_money)} 원)")

# 대출 이자율 입력
interest_rate = st.number_input("대출 이자율 (%)", min_value=0.0, max_value=20.0, step=0.1, format="%.2f")

# 대출 기간 입력
loan_term_years = st.number_input("대출 기간 (년)", min_value=1, max_value=30, step=1)

# 대출 필요 금액 계산
loan_amount = max(price - own_money, 0)

# 월 상환금액 계산 함수 (원리금 균등 상환 방식)
def calculate_monthly_payment(loan_amount, annual_interest_rate, loan_term_years):
    monthly_interest_rate = annual_interest_rate / 100 / 12
    total_months = loan_term_years * 12
    if monthly_interest_rate == 0:
        return loan_amount / total_months
    else:
        monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months) / ((1 + monthly_interest_rate) ** total_months - 1)
        return monthly_payment

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

# 계산 버튼
if st.button("계산하기"):
    if price > 0 and own_money >= 0 and interest_rate >= 0 and loan_term_years > 0:
        # 월 상환금액 계산
        monthly_payment = calculate_monthly_payment(loan_amount, interest_rate, loan_term_years)
        total_payment = monthly_payment * loan_term_years * 12
        total_interest = total_payment - loan_amount

        # 중개 수수료와 취득세 계산
        broker_fee = calculate_broker_fee(price)
        acquisition_tax = calculate_acquisition_tax(price)

        # 결과 출력
        st.write(f"**대출 필요 금액:** {loan_amount:,} 원")
        st.write(f"**월 상환금액 (원리금 균등 상환):** {monthly_payment:,.0f} 원")
        st.write(f"**총 상환 금액:** {total_payment:,.0f} 원")
        st.write(f"**총 이자 부담:** {total_interest:,.0f} 원")
        st.write(f"**부동산 중개 수수료:** {broker_fee:,.0f} 원")
        st.write(f"**취득세:** {acquisition_tax:,.0f} 원")
    else:
        st.write("모든 입력 값을 올바르게 입력해 주세요.")
