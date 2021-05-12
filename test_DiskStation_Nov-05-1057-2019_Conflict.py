

new_txt = eval(data)
# print all_txt
# print new_txt
 
i = 0
for netted in new_txt:
    for x, item in enumerate(netted):
        if type(item) is types.StringType :
            item = item.decode('utf8') 
        sheet.write(i, x, item)
    i += 1
wbk.save("D:/myNumbers.xls") 

