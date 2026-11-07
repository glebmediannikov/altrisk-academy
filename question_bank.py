"""Illustrative prototype question bank; NOT validated for student research.

Six paired items per form. Expand to 12 per form only after educator review,
content validation, and a pilot for equivalent difficulty.
"""
QUESTIONS = {
    'pre': [
        {'id': 'pre01', 'topic': 'diversification', 'prompt': 'Why hold several different investments?', 'options': ('To remove all risk', 'To reduce dependence on one investment', 'To guarantee profit'), 'answer': 'To reduce dependence on one investment'},
        {'id': 'pre02', 'topic': 'liquidity', 'prompt': 'Which asset is usually most accessible for an unexpected bill?', 'options': ('Cash in a savings account', 'A house', 'A long-term locked deposit'), 'answer': 'Cash in a savings account'},
        {'id': 'pre03', 'topic': 'budgeting', 'prompt': 'Income is $100 and spending is $115. What happens?', 'options': ('$15 surplus', '$15 shortfall', 'Balanced budget'), 'answer': '$15 shortfall'},
        {'id': 'pre04', 'topic': 'risk', 'prompt': 'What does a larger possible loss generally indicate?', 'options': ('More downside risk', 'Guaranteed higher return', 'No change in risk'), 'answer': 'More downside risk'},
        {'id': 'pre05', 'topic': 'diversification', 'prompt': 'A portfolio owns only one company. What is a key concern?', 'options': ('Concentration risk', 'No market risk', 'Guaranteed liquidity'), 'answer': 'Concentration risk'},
        {'id': 'pre06', 'topic': 'budgeting', 'prompt': 'What is an emergency fund intended for?', 'options': ('Unplanned expenses', 'Guaranteed investing gains', 'Only luxury purchases'), 'answer': 'Unplanned expenses'},
    ],
    'post': [
        {'id': 'post01', 'topic': 'diversification', 'prompt': 'Why might a mix of unrelated assets be preferable to a single stock?', 'options': ('It eliminates all losses', 'It spreads exposure across investments', 'It guarantees returns'), 'answer': 'It spreads exposure across investments'},
        {'id': 'post02', 'topic': 'liquidity', 'prompt': 'You need to pay an urgent repair tomorrow. Which holding is generally easiest to use?', 'options': ('Money in a savings account', 'An owned home', 'A restricted long-term investment'), 'answer': 'Money in a savings account'},
        {'id': 'post03', 'topic': 'budgeting', 'prompt': 'A town receives $200 and plans $225 of expenses. What is the result?', 'options': ('$25 surplus', '$25 deficit', 'Balanced budget'), 'answer': '$25 deficit'},
        {'id': 'post04', 'topic': 'risk', 'prompt': 'Two investments have the same expected return, but one could lose much more. Which has greater downside exposure?', 'options': ('The one with a larger possible loss', 'Both have no risk', 'The one with a smaller possible loss'), 'answer': 'The one with a larger possible loss'},
        {'id': 'post05', 'topic': 'diversification', 'prompt': 'What risk is especially high if all savings are invested in one company?', 'options': ('Concentration risk', 'Zero volatility', 'Guaranteed safety'), 'answer': 'Concentration risk'},
        {'id': 'post06', 'topic': 'budgeting', 'prompt': 'Why set aside savings for unexpected costs?', 'options': ('To cover emergencies', 'To ensure stock gains', 'To avoid making a budget'), 'answer': 'To cover emergencies'},
    ],
}
