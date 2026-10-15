"""AltRisk Academy climate labs — optional add-on for existing Streamlit app.
Educational, hypothetical values only. Does not fetch securities data.
"""
import math
import pandas as pd
import streamlit as st

GREEN = ['FSLR','NEE','ENPH','BEPC','ICLN','BGRN']
LABELS = {'FSLR':'First Solar — solar manufacturing','NEE':'NextEra Energy — electricity & renewable generation','ENPH':'Enphase Energy — solar technology','BEPC':'Brookfield Renewable — renewable power','ICLN':'iShares Global Clean Energy ETF — renewable equity fund','BGRN':'iShares USD Green Bond ETF — green bond fund'}
SCENARIOS = {
    'Clean energy expansion': {'FSLR':.16,'NEE':.09,'ENPH':.19,'BEPC':.11,'ICLN':.13,'BGRN':.04},
    'Higher interest rates': {'FSLR':-.09,'NEE':-.04,'ENPH':-.19,'BEPC':-.10,'ICLN':-.12,'BGRN':-.03},
    'Economic downturn': {'FSLR':-.24,'NEE':-.13,'ENPH':-.33,'BEPC':-.17,'ICLN':-.22,'BGRN':.01},
    'Mixed transition': {'FSLR':.05,'NEE':.045,'ENPH':-.035,'BEPC':.04,'ICLN':.035,'BGRN':.03},
}


def green_investing(save_score=None):
    st.title('🌱 Green Investing Lab')
    st.caption('Virtual $10,000 · Six fixed securities · No real-money trading')
    with st.expander('📚 Learn: green investing, ESG, diversification and greenwashing', expanded=True):
        st.markdown('**Green investing** supports companies and projects linked to environmental goals. A green company can still be an expensive or risky investment. **ESG** considers environmental, social and governance factors, but ratings and definitions vary. **Green bonds** are debt instruments earmarked for eligible environmental uses; they still face interest-rate and credit risks. **Greenwashing** means presenting environmental claims in a misleading way. **Diversification** reduces concentration but cannot guarantee a profit.')
        st.info('Check both financial risk and environmental claims. Buying a share on the stock exchange usually does not directly fund a new solar project.')
    st.subheader('1 · Allocate your virtual portfolio')
    st.write('Choose one of six predefined securities. All portfolio weights must total 100%.')
    defaults = [20,20,15,15,20,10]
    cols = st.columns(3)
    weights = {}
    for i,ticker in enumerate(GREEN):
        with cols[i%3]:
            weights[ticker] = st.number_input(f'{ticker} allocation (%)', min_value=0, max_value=100, value=defaults[i], step=5, key=f'green_{ticker}', help=LABELS[ticker])
    total = sum(weights.values())
    st.metric('Allocated', f'{total}%')
    if total != 100:
        st.warning('Set allocations to exactly 100% to run the scenario.')
        return
    st.subheader('2 · Test economic conditions')
    scenario = st.selectbox('Hypothetical scenario', list(SCENARIOS))
    years = st.slider('Holding period (years)',1,5,5)
    st.caption('The scenario table assigns hypothetical annual returns for education; these are NOT forecasts or historical returns. The same modeled rate repeats annually, with no rebalancing, tax or fees.')
    rates = SCENARIOS[scenario]
    series=[]
    for year in range(years+1):
        portfolio = sum(10000*(weights[t]/100)*(1+rates[t])**year for t in GREEN)
        series.append({'Year':year,'Portfolio value ($)':portfolio})
    last=series[-1]['Portfolio value ($)']
    top=sorted(weights.items(),key=lambda p:p[1],reverse=True)[0]
    a,b,c=st.columns(3)
    a.metric('Final value', f'${last:,.0f}')
    b.metric('Total return',f'{(last/10000-1)*100:+.1f}%')
    c.metric('Largest single holding',f'{top[1]}%')
    st.line_chart(pd.DataFrame(series).set_index('Year'))
    st.subheader('3 · Compare security outcomes')
    table = pd.DataFrame([{'Security':t,'Theme':LABELS[t].split(' — ')[-1], 'Weight (%)':weights[t], 'Modeled annual change (%)':round(rates[t]*100,1),'Modeled holding value ($)':round(10000*weights[t]/100*(1+rates[t])**years,2)} for t in GREEN])
    st.dataframe(table, hide_index=True, use_container_width=True)
    concentration = sum((w/100)**2 for w in weights.values())
    score = round(max(0,min(100,95-75*concentration-(25 if top[1]>50 else 0))))
    st.info('Important: because the scenario assumes constant annual returns, this curve cannot show realistic volatility or maximum drawdown. The learning score rewards avoiding concentration, not earning higher returns. It is not an ESG score.')
    question=st.radio('Quick check: can a green investment lose money?', ['Choose an answer','Yes, environmental purpose does not remove financial risk','No, green assets are always safe'],key='green_quiz')
    if st.button('Finish Green Investing Lab', type='primary', key='green_finish'):
        if question == 'Yes, environmental purpose does not remove financial risk':
            final=min(100,score+10)
            st.success(f'Well done! Learning score: {final}/100.')
            if save_score: save_score('Green Investing Lab',final,'Green investments can lose value; evaluate concentration, market risks and environmental claims.')
        else: st.warning('Review the green investing explanation and answer the question first.')


def _solar_projection(monthly, coverage, capex, subsidy, growth, upkeep, decline, grid_factor, years):
    no_solar = 0.; with_solar = max(0.,capex-subsidy); results=[]; payback=None
    for y in range(0,years+1):
        if y:
            baseline = monthly*12*(1+growth/100)**(y-1)
            solar_share = min(1.,coverage/100*(1-decline/100)**(y-1))
            no_solar += baseline
            with_solar += baseline*(1-solar_share)+upkeep
            if payback is None and with_solar<=no_solar: payback=y
        results.append({'Year':y,'Without solar ($)':no_solar,'With solar ($)':with_solar})
    avoided_kwh = sum((monthly*12/(grid_factor or 1))*min(1.,coverage/100*(1-decline/100)**(y-1)) for y in range(1,years+1))
    return results,payback,avoided_kwh


def responsible_consumption(save_score=None):
    st.title('🌎 Responsible Consumption Lab')
    st.caption('Compare costs, resources and trade-offs with changeable assumptions.')
    with st.expander('📚 Learn: responsible consumption and climate equity',expanded=True):
        st.markdown('**Responsible consumption** means considering long-term cost, use of resources, waste, and impacts on other people when choosing goods and services. **Payback period** is the time needed for cumulative savings to recover an upfront investment. **Energy efficiency** delivers the same service using less energy. **Climate equity** recognizes that households and neighborhoods have unequal access to money, infrastructure and environmental benefits.')
        st.markdown('This lab is inspired by recommendations in the **Massachusetts Youth Climate Council (2026)** on renewables, energy-efficient buildings, commuting, community gardens, and equitable hands-on climate education.')
    activity=st.radio('Choose an experiment',['🏠 Solar Home','💡 School Lighting','🚍 Commute Challenge','🛍️ Buy, Repair or Replace'],horizontal=True)
    if activity=='🏠 Solar Home':
        st.subheader('🏠 Two identical houses: solar vs. no solar')
        a,b,c=st.columns(3)
        with a:
            monthly=st.slider('Electricity bill before solar ($/month)',50,500,200,10)
            coverage=st.slider('Initial solar coverage (%)',0,100,75,5)
            years=st.slider('Compare over (years)',5,30,20)
        with b:
            capex=st.number_input('Installed cost ($)',0,100000,18000,500)
            subsidy=st.number_input('Modeled rebate / incentive ($)',0,100000,0,250)
            upkeep=st.number_input('Annual maintenance allowance ($)',0,5000,200,50)
        with c:
            growth=st.slider('Grid electricity price growth (%/year)',-3.,10.,3.,.5)
            decline=st.slider('Solar output decline (%/year)',0.,2.,.5,.1)
            price=st.number_input('Electricity price ($/kWh), for emissions estimate',.01,1.,.25,.01)
            kg_per_kwh=st.number_input('Illustrative grid emissions (kg CO₂/kWh)',0.,2.,.30,.05)
        data,payback,kwh=_solar_projection(monthly,coverage,capex,subsidy,growth,upkeep,decline,price,years)
        result=data[-1]
        left,right=st.columns(2)
        with left:
            st.markdown('#### 🏠 Without solar')
            st.metric('Modeled total electricity spending',f'${result["Without solar ($)"]:,.0f}')
        with right:
            st.markdown('#### 🏡 With solar')
            st.metric('Modeled total cost including installation',f'${result["With solar ($)"]:,.0f}')
        x,y,z=st.columns(3)
        x.metric('Modeled net savings',f'${result["Without solar ($)"]-result["With solar ($)"]:,.0f}')
        y.metric('Payback period',f'{payback} years' if payback else f'Not within {years} years')
        z.metric('Estimated emissions avoided',f'{kwh*kg_per_kwh/1000:,.1f} metric tons CO₂')
        st.line_chart(pd.DataFrame(data).set_index('Year'))
        st.caption('Illustrative simplified model. No exports/net metering, financing, taxes, panel replacement, inverter replacement, time-of-use pricing, roof condition or discount rate. Solar panels have lifecycle emissions; avoided operational grid emissions are not net lifecycle benefits. Check real local electricity tariffs and incentive eligibility.')
        check=st.radio('What can make solar financially less attractive?', ['Choose an answer','High installation cost and low electricity savings','The color of the house'],key='solar_check')
        if st.button('Finish Solar Home',key='solar_done',type='primary'):
            if check=='High installation cost and low electricity savings':
                st.success('Great! You considered costs and uncertainty.')
                if save_score: save_score('Responsible Consumption Lab',90,'Compared solar and non-solar homes, including payback and climate assumptions.')
            else:st.warning('Try the knowledge check first.')
    elif activity=='💡 School Lighting':
        st.subheader('💡 Modernize classroom lighting')
        st.write('Compare running costs of hypothetical lighting systems. The YCC report recommends more natural lighting and adjustable LED use in schools.')
        count=st.slider('Number of fixtures',10,500,100,10)
        hours=st.slider('Daily usage (hours)',1,16,8)
        days=st.slider('Operating days per year',100,365,180)
        old=st.slider('Existing fixture power (W)',20,160,80,5)
        new=st.slider('LED fixture power (W)',5,120,40,5)
        kwh_cost=st.slider('Electricity price ($/kWh)',.10,.60,.25,.01)
        upgrade=st.number_input('Upgrade cost ($)',0,100000,5000,500)
        annual=(old-new)*count*hours*days/1000*kwh_cost
        aa,bb=st.columns(2)
        aa.metric('Annual electricity savings',f'${annual:,.0f}')
        bb.metric('Simple payback',f'{upgrade/annual:.1f} years' if annual>0 else 'No modeled savings')
        st.caption('Electricity only: excludes lamp replacement, HVAC changes, installation disruptions, financing and quality-of-light differences.')
    elif activity=='🚍 Commute Challenge':
        st.subheader('🚍 How do you travel to school?')
        miles=st.slider('Round-trip miles per day',2,80,20)
        days=st.slider('Travel days per year',20,250,180)
        fuel=st.slider('Gasoline price ($/gallon)',2.,7.,3.5,.25)
        efficiency=st.slider('Car fuel economy (miles/gallon)',15,60,30)
        transit=st.slider('Daily public transit ticket cost ($)',0.,20.,4.,.5)
        annual_gas=miles*days/efficiency*fuel
        annual_transit=days*transit
        st.bar_chart(pd.DataFrame({'Yearly out-of-pocket cost ($)': [annual_gas,annual_transit]},index=['Car: fuel only','Public transport: fares only']))
        st.caption('Not a full transport lifecycle comparison. Excludes vehicle purchase, insurance, maintenance, parking, electricity, embodied emissions, and route availability. Public transport options differ by location.')
    else:
        st.subheader('🛍️ Buy, repair or replace?')
        st.write('A school bag breaks. Compare its total expected cost over four years.')
        cheap=st.slider('Cheap replacement bag price ($)',10,120,30,5)
        durable=st.slider('Durable bag price ($)',30,250,100,5)
        repair=st.slider('Repair existing bag ($)',0,100,20,5)
        st.bar_chart(pd.DataFrame({'4-year example cost ($)':[cheap*4,durable,repair]},index=['Replace annually','Buy durable once','Repair once']))
        st.caption('Hypothetical lifetimes: replace the cheap bag once annually, durable bag lasts 4 years, repaired existing bag lasts 4 years. These lifetimes are uncertain; recycling, environmental impact and actual product performance vary.')
    st.divider()
    st.caption('Source of policy inspiration: Massachusetts Youth Climate Council, Climate Recommendations, May 29, 2026. This independent educational game is not an official government platform.')
