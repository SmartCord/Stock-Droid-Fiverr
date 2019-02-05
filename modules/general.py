from imports import * 

class General:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx, *, query: str = None):
        if query is None:
            return await usage(ctx, ['symbol'], ['wdc'])
        
        page = "http://finance.yahoo.com/quote/{}".format(query.upper())
        req = requests.get(page)
        seperator = "•"
        datas = []
        
        bs = soup(req.text, 'html.parser')
        cfs = bs.find('div', id="quoteNewsStream-0-Stream-Proxy")
        if cfs is None:
            page = "https://finviz.com/search.ashx?p={}".format(query.upper())
            r = requests.get(page)
            page = r.text 
            bs = soup(page, 'html.parser')
            main_table = bs.find('table', attrs={'class':'styled-table'})
            if main_table is None:
                e = embed(ctx, f"No results found for {query}", "Please make sure you're typing it correctly")
                return await ctx.send(embed=e)
                
            body = main_table.find_all('tr')[1].find_all('td')[0].text
            e = embed(ctx, title=f"No results found for {query}", description=f"Maybe you meant {body}?")
            return await ctx.send(embed=e)

        for item in cfs.find_all('li', attrs={'class':'js-stream-content'}):
            val1 = item.find('div', attrs={'class':'Fz(11px)'})
            val1s = val1.text.split('•')
            author = val1s[0]
            time = val1s[1]

            title = item.find('h3', attrs={'class':'Mb(5px)'})
            href = title.a['href']
            description = item.find('p', attrs={'class':'Fz(14px)'})
            
            if len(description.text) >= 200:
                desc = description.text[:199] + "..."
            else:
                desc = description.text

            datas.append({
                "author": author,
                "time": time,
                "title": title.text,
                "href":href,
                "description":desc
            })

        embeds = []
        
        pg = commands.Paginator(prefix="", suffix="", max_size=1022)
        i = 1
        for data in datas:
            desc = data['description']
            item = f"""
{i}. {data['author']} {seperator} {data['time']}
[{data['title']}](https://finance.yahoo.com{data['href']})
{desc}
"""         
            pg.add_line(item)
            i += 1

        i = 1
        for page in pg.pages:
            e = embed(title=f"News about {query.upper()}", description=page, ctx=ctx)
            embeds.append(e)
            i += 1
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def info(self, ctx, *, query: str = None):
        if query is None:
            return await usage(ctx, ['symbol'], ['cgc'])
        
        dataToScrape = [
            'Prev Close AA',
            'Open',
            'After Market',
            'Change Percent AA',
            'Market Cap AA',
            'Dividend % AA',
            'Volume AA',
            'Average Volume AA',
            'Day Range AA',
            '52 Week Range AA',
            'Performance Week Month Quarted YTD AA',
            'Relative Volume AA',
            'Short Float AA',
            'Earnings AA'
        ]

        page = requests.get(f"https://finviz.com/quote.ashx?t={query.upper()}").text 
        bs = soup(page, 'html.parser')
        table = bs.find('table', attrs={'class':'snapshot-table2'})
        datas = []
        if table is None:
            page = "https://finviz.com/search.ashx?p={}".format(query.upper())
            r = requests.get(page)
            page = r.text 
            bs = soup(page, 'html.parser')
            main_table = bs.find('table', attrs={'class':'styled-table'})
            if main_table is None:
                e = embed(ctx, f"No results found for {query}", "Please make sure you're typing it correctly")
                return await ctx.send(embed=e)
                
            body = main_table.find_all('tr')[1].find_all('td')[0].text
            e = embed(ctx, title=f"No results found for {query}", description=f"Maybe you meant {body}?")
            return await ctx.send(embed=e)
        
        filters = ['Market Cap', 'Dividend %', 'Short Float', '52W Range', 'Prev Close', 'Change', 'Rel Volume', 'Avg Volume', 'Perf Week', 'Perf Month', 'Perf Quarter', 'Perf YTD', 'Earnings', 'Price']
        perfs = []
        datas = []
        rows = table.find_all('tr')
        price = "undefined"
        for row in rows:
            names = row.find_all('td', attrs={'class':'snapshot-td2-cp'})
            values = row.find_all('td', attrs={'class':'snapshot-td2'})

            for name, value in zip(names, values):
                if name.text in filters:
                    if name.text == 'Price':
                        price = value.text 
                    elif name.text in ('Perf Week', 'Perf Month', 'Perf Quarter', 'Perf YT'):
                        perfs.append(f"{name.text.split()[1]} : {value.text}")
                    else:
                        data = {name.text, value.text}
                        datas.append(data)
                        
        company = bs.find('table', attrs={'class':'fullview-title'}).select('tr:nth-child(2)')[0].text
        faviconA = bs.select('table.fullview-title tr:nth-child(2) a')[0]['href']
        faviconX = favicon.get(faviconA)[0]
        page = f"https://finance.yahoo.com/quote/{query.upper()}?p={query.upper()}"
        bs = soup(requests.get(page).text, 'html.parser')   


        e = embed(ctx, f'{company} is currently at ${price}', description=query.upper(), customThumbnail=faviconX.url)
        await ctx.send(embed=e)


    @commands.command()
    async def chart(self, ctx, *, query: str = None):
        if query is None:
            return await usage(ctx, ['symbol'], ['cgc'])
        
        page = "https://finviz.com/quote.ashx?t=" + query.upper()
        r = requests.get(page)
        page = r.text 

        bs = soup(page, 'html.parser')
        img = bs.find('img', id="chart0")
        if img is None:
            page = "https://finviz.com/search.ashx?p={}".format(query.upper())
            r = requests.get(page)
            page = r.text 
            bs = soup(page, 'html.parser')
            main_table = bs.find('table', attrs={'class':'styled-table'})
            if main_table is None:
                e = embed(ctx, f"No results found for {query}", "Please make sure you're typing it correctly")
                return await ctx.send(embed=e)
                
            body = main_table.find_all('tr')[1].find_all('td')[0].text
            e = embed(ctx, title=f"No results found for {query}", description=f"Maybe you meant {body}?")
            return await ctx.send(embed=e)

        img = "https://finviz.com/" + img['src']
        
        e = embed(ctx, title=f"Chart for {query.upper()}", image=img)
        await ctx.send(embed=e)

    @commands.command()
    async def highs(self, ctx, *, query: str = None):
        if query is None:
            page = "https://finviz.com/screener.ashx?v=110&s=ta_newhigh"
            base = "https://finviz.com/"
            page = requests.get(page).text
            bs = soup(page, 'html.parser')
            rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
            datas = []
            for row in rows:
                td = row.find_all('td')
                ticker = td[1]
                name = td[2]
                cap = td[6]
                pe = td[7]
                price = td[8]
                change = td[9]
                volume = td[10]
                data = {
                    "ticker":ticker.text,
                    "href":ticker.find('a')['href'],
                    "name":name.text,
                    "price":price.text,
                    "change":change.text,
                    "market_cap":cap.text,
                    "P/E":pe.text,
                    "volume":volume.text 
                }
                datas.append(data)
            
            pg = commands.Paginator(prefix="", suffix="", max_size=500)

            for data in datas:
                pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

            embeds = []
            for page in pg.pages:
                e = embed(ctx, "New Highs", page)
                embeds.append(e)
            
            p = utils.Paginator(ctx, embeds=embeds)
            await p.paginate()
            return 


        page = "https://finance.yahoo.com/quote/{}/history?p={}".format(query.upper(), query.upper())
        r = requests.get(page)
        page = r.text
        bs = soup(page, 'html.parser')
        table = bs.find('table', attrs={'data-test':'historical-prices'})
        if table is None:
            page = "https://finviz.com/search.ashx?p={}".format(query.upper())
            r = requests.get(page)
            page = r.text 
            bs = soup(page, 'html.parser')
            main_table = bs.find('table', attrs={'class':'styled-table'})
            if main_table is None:
                e = embed(ctx, f"No results found for {query}", "Please make sure you're typing it correctly")
                return await ctx.send(embed=e)
                
            body = main_table.find_all('tr')[1].find_all('td')[0].text
            e = embed(ctx, title=f"No results found for {query}", description=f"Maybe you meant {body}?")
            return await ctx.send(embed=e)

        datas = []
        
        tbody = table.find('tbody')
        for rows in tbody.find_all('tr'):
            tdata = rows.find_all('td')
            try:
                date = tdata[0].text
                high = tdata[2].text 
                data = {"date": date, "high":high}
                print(data)
                datas.append(data)
            except IndexError:
                pass

        pg = commands.Paginator(prefix="", suffix="", max_size=300)
        for data in datas:
            pg.add_line(f"**{data['date']}**\nHigh : {data['high']}\n") 
        
        embeds = []
        for page in pg.pages:
            embeds.append(embed(ctx, f"New highs for {query.upper()}", page))
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def lows(self, ctx, *, query: str = None):
        if query is None:
            page = "https://finviz.com/screener.ashx?v=110&s=ta_newlow"
            base = "https://finviz.com/"
            page = requests.get(page).text
            bs = soup(page, 'html.parser')
            rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
            datas = []
            for row in rows:
                td = row.find_all('td')
                ticker = td[1]
                name = td[2]
                cap = td[6]
                pe = td[7]
                price = td[8]
                change = td[9]
                volume = td[10]
                data = {
                    "ticker":ticker.text,
                    "href":ticker.find('a')['href'],
                    "name":name.text,
                    "price":price.text,
                    "change":change.text,
                    "market_cap":cap.text,
                    "P/E":pe.text,
                    "volume":volume.text 
                }
                datas.append(data)
            
            pg = commands.Paginator(prefix="", suffix="", max_size=500)

            for data in datas:
                pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

            embeds = []
            for page in pg.pages:
                e = embed(ctx, "New Lows", page)
                embeds.append(e)
            
            p = utils.Paginator(ctx, embeds=embeds)
            await p.paginate()
            return
        
        page = "https://finance.yahoo.com/quote/{}/history?p={}".format(query.upper(), query.upper())
        r = requests.get(page)
        page = r.text
        bs = soup(page, 'html.parser')
        table = bs.find('table', attrs={'data-test':'historical-prices'})
        if table is None:
            page = "https://finviz.com/search.ashx?p={}".format(query.upper())
            r = requests.get(page)
            page = r.text 
            bs = soup(page, 'html.parser')
            main_table = bs.find('table', attrs={'class':'styled-table'})
            if main_table is None:
                e = embed(ctx, f"No results found for {query}", "Please make sure you're typing it correctly")
                return await ctx.send(embed=e)
                
            body = main_table.find_all('tr')[1].find_all('td')[0].text
            e = embed(ctx, title=f"No results found for {query}", description=f"Maybe you meant {body}?")
            return await ctx.send(embed=e)

        datas = []
        
        tbody = table.find('tbody')
        for rows in tbody.find_all('tr'):
            tdata = rows.find_all('td')
            try:
                date = tdata[0].text
                high = tdata[3].text 
                data = {"date": date, "low":high}
                print(data)
                datas.append(data)
            except IndexError:
                pass

        pg = commands.Paginator(prefix="", suffix="", max_size=300)
        for data in datas:
            pg.add_line(f"**{data['date']}**\nLow : {data['low']}\n") 
        
        embeds = []
        for page in pg.pages:
            embeds.append(embed(ctx, f"New low for {query.upper()}", page))
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def trending(self, ctx):
        page = "https://finance.yahoo.com/trending-tickers/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        table = bs.find('table', attrs={'class':'yfinlist-table'}).find('tbody')
        datas = []
        index = 1

        for row in table.find_all('tr'):
            info = row.find_all('td')
            symbol = info[0].text
            name = info[1].text
            last_price = info[2].text
            volume = info[6].text
            market_cap = info[8].text

            data = {
                "symbol":symbol,
                "name":name,
                "last_price":last_price,
                "volume":volume,
                "market_cap":market_cap 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=400)
        for data in datas:
            d = f"""
**{data['symbol']}**
{data['name']}
Last Price : {data['last_price']}
Volume : {data['volume']}
Market Cap : {data['market_cap']}"""     
            pg.add_line(d)

        embeds = []
        for description in pg.pages:
            e = embed(ctx, "Trending Tickers", description)
            embeds.append(e)

        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def options(self, ctx, *, query: str = None):
        if query is None:
            return await usage(ctx, ['symbol'], ['cgc'])
        
        page = f"https://marketchameleon.com/Overview/{query.upper()}/OptionSummary/OpenInterest"
        page = requests.get(page).text

        bs = soup(page, 'html.parser')
        table = bs.find(id="option_summary_OpenInt")
        if table is None:
            page = "https://finviz.com/search.ashx?p={}".format(query.upper())
            r = requests.get(page)
            page = r.text 
            bs = soup(page, 'html.parser')
            main_table = bs.find('table', attrs={'class':'styled-table'})
            if main_table is None:
                e = embed(ctx, f"No results found for {query}", "Please make sure you're typing it correctly")
                return await ctx.send(embed=e)
                
            body = main_table.find_all('tr')[1].find_all('td')[0].text
            e = embed(ctx, title=f"No results found for {query}", description=f"Maybe you meant {body}?")
            return await ctx.send(embed=e)
        datas = []
        
        tbody = table.find('tbody')
        for row in tbody.find_all('tr'):
            item = row.find_all('td')
            expiration = item[0].text 
            oi = item[1].text 
            call = item[7].text 
            put = item[8].text 
            data = {
                "expiration":expiration,
                "oi":oi,
                "call":call,
                "put":put
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=400)
        for data in datas:
            pg.add_line(f"""
Expiration : {data['expiration']}
Open Interest : {data['oi']}
% Call : {data['call']}
% Put : {data['put']}""")

        embeds = []
        for desc in pg.pages:
            e = embed(ctx, f"Open Interest", desc)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def earnings_old(self, ctx):
        page = "https://finviz.com/screener.ashx?v=110&s=n_earningsafter&f=sh_curvol_o1000"
        base = "https://finviz.com/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        try:
            rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
        except IndexError:
            e = embed(ctx, "No earnings")
            return await ctx.send(embed=e)
        datas = []
        try:
            for row in rows:
                td = row.find_all('td')
                ticker = td[1]
                name = td[2]
                cap = td[6]
                pe = td[7]
                price = td[8]
                change = td[9]
                volume = td[10]
                data = {
                    "ticker":ticker.text,
                    "href":ticker.find('a')['href'],
                    "name":name.text,
                    "price":price.text,
                    "change":change.text,
                    "market_cap":cap.text,
                    "P/E":pe.text,
                    "volume":volume.text 
                }
                datas.append(data)
        except IndexError:
            e = embed(ctx, "No Earnings to show")
            return await ctx.send(embed=e)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=500)

        for data in datas:
            pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Earnings", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def earnings(self, ctx, data: str = None):
        if data is None:
            return await usage(ctx, ['tomorrow or today'], ['tomorrow'])
        
        similarity1 = utils.similar(data.upper(), "TOMORROW")
        similarity2 = utils.similar(data.upper(), "TODAY")

        if similarity1 >= 0.7:
            dataType = 0
            title = "tomorrow"
        elif similarity2 >= 0.7:
            dataType = 1 
            title = "today"
        else:
            e = embed(ctx, "Invalid Argument", "Argument must be either tomorrow or today", customColor="red")
            return await ctx.send(embed=e)
        
        default = "Bgc($lightBlue)"
        base = "https://finance.yahoo.com"

        page = "https://finance.yahoo.com/calendar/earnings"
        page = requests.get(page).text
        bs = soup(page, 'html.parser')
        ul = bs.find('ul', attrs={'class':'Bd(0)--tab768'})
        forTomorrow = False

        for li in ul.find_all('li'):
            if default in li['class']:
                if dataType == 1:
                    page = li.find('a')
                    if page is None:
                        e = embed(ctx, "No earnings for today")
                        await ctx.send(embed=e)
                        return 

                    page = base + page['href']
                elif dataType == 0:
                    forTomorrow = True 
            else:
                if forTomorrow:
                    page = li.find('a')
                    print(page)
                    if page is None:
                        e = embed(ctx, "No earnings for tomorrow")
                        await ctx.send(embed=e)
                        return

                    page = base + page['href']
                    break 
        
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        table = bs.find('table', attrs={'class':'data-table'}).find('tbody')
        datas = []

        for row in table.find_all('tr'):
            td = row.find_all('td')
            symbol = td[0]
            company = td[1]
            call_time = td[2]
            eps_estimate = td[3]

            data = {
                "symbol":symbol.text,
                "symbol_href":symbol.find("a")['href'],
                "company":company.text,
                "ect":call_time.text,
                "eps":eps_estimate.text
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=600)
        for data in datas:
            pg.add_line(f"""
[{data['symbol']}]({base + data['symbol_href']})
{data['company']}
Call Time : {data['ect']}
EPS Estimate : {data['eps']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, f"Earnings for {title}", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def gainers(self, ctx):
        page = "https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        table = bs.find('table', attrs={'class':'tv-data-table'}).find('tbody')
        base = "https://www.tradingview.com"
        datas = []
        for rows in table.find_all('tr'):
            td = rows.find_all('td')
            symbol = td[0]
            last = td[1]
            change = td[3]
            rating = td[4]
            volume = td[5]

            data = {
                "symbol":symbol.find('a').text ,
                "href":symbol.find('a')['href'],
                "name":symbol.find('span', attrs={'class':'tv-screener__description'}).text,
                "last":last.text,
                "change":change.text,
                "rating":rating.text,
                "volume":volume.text 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=600)
        for data in datas:
            pg.add_line(f"""
[{data['symbol']}]({base + data['href']}){data['name']}
Last : {data['last']}
Change : {data['change']}
Rating : {data['rating']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Top Gainers", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def losers(self, ctx):
        page = "https://www.tradingview.com/markets/stocks-usa/market-movers-losers/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        table = bs.find('table', attrs={'class':'tv-data-table'}).find('tbody')
        base = "https://www.tradingview.com"
        datas = []
        for rows in table.find_all('tr'):
            td = rows.find_all('td')
            symbol = td[0]
            last = td[1]
            change = td[3]
            rating = td[4]
            volume = td[5]

            data = {
                "symbol":symbol.find('a').text ,
                "href":symbol.find('a')['href'],
                "name":symbol.find('span', attrs={'class':'tv-screener__description'}).text,
                "last":last.text,
                "change":change.text,
                "rating":rating.text,
                "volume":volume.text 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=600)
        for data in datas:
            pg.add_line(f"""
[{data['symbol']}]({base + data['href']}){data['name']}
Last : {data['last']}
Change : {data['change']}
Rating : {data['rating']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Top Losers", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def unusual(self, ctx):
        page = "https://finviz.com/screener.ashx?v=110&s=ta_unusualvolume"
        base = "https://finviz.com/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
        print(rows)
        datas = []
        for row in rows:
            td = row.find_all('td')
            ticker = td[1]
            name = td[2]
            cap = td[6]
            pe = td[7]
            price = td[8]
            change = td[9]
            volume = td[10]
            data = {
                "ticker":ticker.text,
                "href":ticker.find('a')['href'],
                "name":name.text,
                "price":price.text,
                "change":change.text,
                "market_cap":cap.text,
                "P/E":pe.text,
                "volume":volume.text 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=500)

        for data in datas:
            pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Unusual Volume", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def downgrades(self, ctx):
        page = "https://finviz.com/screener.ashx?v=110&s=n_downgrades"
        base = "https://finviz.com/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
        print(rows)
        datas = []
        for row in rows:
            td = row.find_all('td')
            ticker = td[1]
            name = td[2]
            cap = td[6]
            pe = td[7]
            price = td[8]
            change = td[9]
            volume = td[10]
            data = {
                "ticker":ticker.text,
                "href":ticker.find('a')['href'],
                "name":name.text,
                "price":price.text,
                "change":change.text,
                "market_cap":cap.text,
                "P/E":pe.text,
                "volume":volume.text 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=500)

        for data in datas:
            pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Downgrades", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def upgrades(self, ctx):
        page = "https://finviz.com/screener.ashx?v=110&s=n_upgrades"
        base = "https://finviz.com/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
        print(rows)
        datas = []
        for row in rows:
            td = row.find_all('td')
            ticker = td[1]
            name = td[2]
            cap = td[6]
            pe = td[7]
            price = td[8]
            change = td[9]
            volume = td[10]
            data = {
                "ticker":ticker.text,
                "href":ticker.find('a')['href'],
                "name":name.text,
                "price":price.text,
                "change":change.text,
                "market_cap":cap.text,
                "P/E":pe.text,
                "volume":volume.text 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=500)

        for data in datas:
            pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Upgrades", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def overbought(self, ctx):
        page = "https://finviz.com/screener.ashx?v=110&s=ta_overbought"
        base = "https://finviz.com/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
        print(rows)
        datas = []
        for row in rows:
            td = row.find_all('td')
            ticker = td[1]
            name = td[2]
            cap = td[6]
            pe = td[7]
            price = td[8]
            change = td[9]
            volume = td[10]
            data = {
                "ticker":ticker.text,
                "href":ticker.find('a')['href'],
                "name":name.text,
                "price":price.text,
                "change":change.text,
                "market_cap":cap.text,
                "P/E":pe.text,
                "volume":volume.text 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=500)

        for data in datas:
            pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Overbought", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def oversold(self, ctx):
        page = "https://finviz.com/screener.ashx?v=110&s=ta_oversold"
        base = "https://finviz.com/"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')
        rows = bs.find(id='screener-content').find('table').find_all('tr')[5].find('td').find('table').find_all('tr')[1:]
        datas = []
        for row in rows:
            td = row.find_all('td')
            ticker = td[1]
            name = td[2]
            cap = td[6]
            pe = td[7]
            price = td[8]
            change = td[9]
            volume = td[10]
            data = {
                "ticker":ticker.text,
                "href":ticker.find('a')['href'],
                "name":name.text,
                "price":price.text,
                "change":change.text,
                "market_cap":cap.text,
                "P/E":pe.text,
                "volume":volume.text 
            }
            datas.append(data)
        
        pg = commands.Paginator(prefix="", suffix="", max_size=500)

        for data in datas:
            pg.add_line(f"""
[{data['ticker']}]({base + data['href']})
{data['name']}
Price : {data['price']}
Change : {data['change']}
P/E : {data['P/E']}
Market Cap : {data['market_cap']}
Volume : {data['volume']}""")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Overbought", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def halts(self, ctx):
        page = "https://markets.cboe.com/us/equities/market_statistics/halts/"
        page = requests.get(page).text
        bs = soup(page, 'html.parser')
        try:
            rows = bs.find_all('table', attrs={'class':'bats-table'})[1].find('tbody').find_all('tr')
        except IndexError:
            return await ctx.send(embed=embed(ctx, "Halts", "No halts found for today"))
        datas = []

        for row in rows:
            td = row.find_all('td')
            symbol = td[0].text
            name = td[1].text
            market = td[2].text
            halt = td[3].text
            reason = td[4].text 
            resume_date = td[5].text 
            quote_time = td[6].text 
            resume_time = td[7].text 

            data = {
                "symbol":symbol,
                "href":f"https://finviz.com/quote.ashx?t={symbol}",
                "name":name,
                "market":market,
                "halt":halt,
                "reason":reason if reason != "" else "-",
                "resume_date":resume_date if resume_date != "" else "-",
                "quote_time":quote_time if quote_time != "" else "-",
                "resume_time":resume_date if resume_date != "" else "-"
            }
            datas.append(data)

        pg = commands.Paginator(prefix="", suffix="", max_size=700)
        embeds = []
        for data in datas:
            pg.add_line(f"""
[{data['symbol']}]({data['href']})
{data['name']}
Market : {data['market']}
Halt : {data['halt']}
Reason : {data['reason']}
Resume Date : {data['resume_date']}
Quote Time : {data['quote_time']}
Resume Time : {data['resume_time']}""")

        for page in pg.pages:
            e = embed(ctx, "Halts", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command()
    async def heatmap(self, ctx):
        page = requests.get("https://finviz.com/groups.ashx").text 
        bs = soup(page, 'html.parser')
        heatMap = "https://finviz.com/" + bs.find_all('td', attrs={'align':'center'})[8].find_all('img')[0]['src']
        e = embed(ctx, "Heatmap", image=heatMap)
        await ctx.send(embed=e)

    @commands.command()
    async def sec_old(self, ctx, *, query:str = None):
        if query is None:
            return await usage(ctx, ['symbol'], ['cgc'])

        page = requests.get(f"https://www.nasdaq.com/symbol/{query.upper()}/sec-filings").text
        bs = soup(page, 'html.parser')
        frame = bs.find(id='quotes_content_left_pdata')
        if frame is None:
            page = "https://finviz.com/search.ashx?p={}".format(query.upper())
            r = requests.get(page)
            page = r.text 
            bs = soup(page, 'html.parser')
            main_table = bs.find('table', attrs={'class':'styled-table'})
            if main_table is None:
                e = embed(ctx, f"No results found for {query}", "Please make sure you're typing it correctly")
                return await ctx.send(embed=e)
                
            body = main_table.find_all('tr')[1].find_all('td')[0].text
            e = embed(ctx, title=f"No results found for {query}", description=f"Maybe you meant {body}?")
            return await ctx.send(embed=e)

        iframe = frame.find('iframe')['src'].replace(' ', "")
        page = requests.get(iframe, verify=False).text
        bs = soup(page, 'html.parser')

        table = bs.find('table').find_all('tr')[1].find_all('td')[1].find_all('table')[2].find_all('tr')[2:]
        datas = []

        for row in table:
            print(row)

    @commands.command()
    async def ssr(self, ctx):
        page = "https://www.nasdaqtrader.com/trader.aspx?id=shortsalecircuitbreaker"
        page = requests.get(page).text 
        bs = soup(page, 'html.parser')

        table = bs.find_all('div', attrs={'class':'genTable'})[2].find('table').find_all('tr')[1:]
        datas = []
        try:
            for row in table:
                td = row.find_all('td')
                symbol = td[0].text 
                name = td[1].text
                market = td[2].text
                time = td[3].text

                data = {
                    "symbol":symbol,
                    "href":f"https://finviz.com/quote.ashx?t={symbol}",
                    "name":name,
                    "market":market,
                    "time":time 
                }
                datas.append(data)
        except IndexError:
            e = embed(ctx, "There's nothing to show here.")
            return await ctx.send(embed=e)

        pg = commands.Paginator(prefix="", suffix="", max_size=700)
        embeds = []

        for d in datas:
            pg.add_line(f"""
[{d['symbol']}]({d['href']})
{d['name']}
Market Category : {d['market']}
Trigger Time : {d['time']}""")

        for page in pg.pages:
            e = embed(ctx, "Short Sale Circuit Breaker", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

    @commands.command(name="commands")
    async def _commands(self, ctx):
        p = utils.returnPrefix()
        cmds = ["news <symbol>", "info <symbol>", "chart <symbol>", "highs <symbol>", "lows <symbol>", "trending", "options <symbol>", "earnings", "gainers", "losers", "unusual", "downgrades", "upgrades", "overbought", "oversold", "halts", "heatmap", "ssr"]

        pg = commands.Paginator(prefix="", suffix="", max_size=150)
        for cmd in cmds:
            pg.add_line(p + cmd + "\n")

        embeds = []
        for page in pg.pages:
            e = embed(ctx, "Command List", page)
            embeds.append(e)
        
        p = utils.Paginator(ctx, embeds=embeds)
        await p.paginate()

def setup(bot):
    bot.add_cog(General(bot))