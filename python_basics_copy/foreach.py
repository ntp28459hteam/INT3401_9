fruits = ['apples','oranges','pears','bananas']
for fruit in fruits:
    print fruit + ' for sale'
    
fruitPrices = {'apples':2.00, 'oranges': 1.50, 'pears': 1.75}
for fruit, price in fruitPrices.items():
    print '%s cost %.2f a pound' % (fruit, price)
    
companies = ['IBM', 'Intel', 'AMD']
for company in companies:
    print company
