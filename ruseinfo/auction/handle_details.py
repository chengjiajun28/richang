import re

import pandas as pd
from bs4 import BeautifulSoup


def handle(*args, **kwargs):
    website = kwargs.get("website")
    row = kwargs.get("row")

    if website == "ccgp_gov_qt":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到要删除的 div 标签，并删除
        div_to_delete = soup.find('div', attrs={'class': 'bid_attachtab'})
        if div_to_delete:
            div_to_delete.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == "ccgp_gov_dy":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])

        soup = BeautifulSoup(row_value, 'html.parser')

        p_to_delete = soup.find('p', string='    附件：')
        if p_to_delete:
            for sibling in p_to_delete.find_next_siblings():
                sibling.extract()
            p_to_delete.extract()

        for i in range(1, 10):
            soup = str(soup).replace(f"（{i}）", "")

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = soup

        return row

    if website == "wypai":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x公告内容'])

        # 使用BeautifulSoup解析HTML源代码
        soup = BeautifulSoup(row_value, 'html.parser')

        # 删除所有的img标签
        for img in soup.find_all('img'):
            img.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x公告内容'] = soup.prettify()

        return row

    if website == "sotcbb_zc":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])

        # 使用BeautifulSoup解析HTML源代码
        soup = BeautifulSoup(row_value, 'html.parser')

        # 删除所有的img标签
        for img in soup.find_all('a'):
            img.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = soup.prettify()

        return row

    if website == "m_gscq_com_cn_fj" or website == "m_gscq_com_cn_fj":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])

        # 使用BeautifulSoup解析HTML源代码
        soup = BeautifulSoup(row_value, 'html.parser')

        # 查找所有的table标签中有第一个td是"标"的tr，并将其删除
        for tr in soup.select('table tr'):
            if tr.select_one('td').text.replace(" ", "").replace("\n", "").replace("\t", "") == '附件下载':
                tr.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = soup.prettify()

        return row

    if website == "bid_norincogroup-ebuy":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        for tag in soup.find_all('iframe'):
            tag['height'] = '86vh'

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == 'otc_cbex_zc_qt':

        # 获取字段值并转换为字符串类型
        row_value = str(row['x交易条件'])

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到要删除的 div 标签，并删除
        for img_tag in soup.find_all('img'):
            img_tag.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x交易条件'] = str(soup)

        # 获取字段值并转换为字符串类型
        row_value = str(row['x交易条件'])

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到要删除的 div 标签，并删除
        for img_tag in soup.find_all('a'):
            img_tag.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x交易条件'] = str(soup)

        return row  # x交易条件与受让方资格条件

    if website == "otc_cbex_zc_jx":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x交易条件与受让方资格条件'])

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到要删除的 div 标签，并删除
        for img_tag in soup.find_all('img'):
            img_tag.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x交易条件与受让方资格条件'] = str(soup)

        return row  #

    if website == "hsjcq_sw":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到要删除的 div 标签，并删除
        for img_tag in soup.find_all('img'):
            img_tag.extract()
        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    # ----------10.19
    if website == "portal_ntree_zs" or website == "portal_ntree_xz":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        for tag in soup.find_all('th'):
            tag['style'] = 'min-width: 120px;'
        for img_tag in soup.find_all('a'):
            img_tag.extract()
        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == "swueecg_jj":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        for tag in soup.find_all('a', href=True):
            tag.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情信息'] = str(soup)

        return row

    if website == "laipaiya_sf_jx":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x拍卖详情'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('div',
                                 class_="entrust-detail-auction-info-item dl ng-star-inserted"):  # class="entrust-detail-auction-info-item dl ng-star-inserted"
            div['style'] = 'display:flex;'

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x拍卖详情'] = str(soup)

        return row

    if website == "qhcqjy_gy_sb":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('img'):
            div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == "rmfysszc_sb":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x拍卖公告'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性

        for div in soup.find_all('a'):
            div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x拍卖公告'] = str(soup)

        # 获取字段值并转换为字符串类型
        row_value = str(row['x标的介绍'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('img'):
            div.extract()
        for div in soup.find_all('video'):
            div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x标的介绍'] = str(soup)

        return row

    if website == "sgcc_zb":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('a'):
            div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == "dscq_fj":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('a'):
            div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == "crccsc_xh":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x竞价要求'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('div', class_="index__reuse_row--ijkgd"):
            div['style'] = 'display:flex;'

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x竞价要求'] = str(soup)

        return row

    if website == "epec_yj_jj":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('a'):
            div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == "cdggzy_zc":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 给每个div标签添加属性
        for div in soup.find_all('a'):
            div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup)

        return row

    if website == "ouyeel":  # 单项

        # 获取字段值并转换为字符串类型
        row_value = str(row['x联系信息'])  # x竞价须知

        # 使用 Beautiful Soup 解析 HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到倒数第二个<tr>标签
        tr_tag = soup.find_all('tr')[-2]

        # 删除倒数第二个<tr>标签
        tr_tag.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x联系信息'] = str(soup)

        return row

    if website == "zy_yunshang_wz":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情信息'])  # x竞价须知

        soup = BeautifulSoup(row_value, 'html.parser')

        for p_tag in soup.find_all('p'):
            if p_tag.find('span') and p_tag.find('span').find('font') and p_tag.find('span').find('font').find(
                    'img'):
                p_tag.unwrap()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情信息'] = str(soup.prettify())

        return row

    if website == "zy_yunshang_fzb":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情信息'])  # x竞价须知

        soup = BeautifulSoup(row_value, 'html.parser')

        for tag in soup.find_all('strong'):
            tag.unwrap()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情信息'] = str(soup.prettify())

        return row

    if website == "srmmx_wz":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x物的介绍'])  # x竞价须知

        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到所有class为"clearfix"的div标签
        div_list = soup.find_all('div', class_="clearfix")

        # 删除倒数两个div标签
        for div in div_list[-2:]:
            div.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x物的介绍'] = str(soup.prettify())

        return row

    if website == "srm_easthope":
        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 查找并删除id为"biddingDocuments"的div标签
        div = soup.find('div', {'id': 'biddingDocuments'})
        div.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "news_lzit_tz":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 创建BeautifulSoup对象
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到具有特定属性的p标签
        p_tags = soup.find_all('p', attrs={'style': 'text-align: center'})

        # 删除这些p标签
        for p_tag in p_tags:
            p_tag.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "srm_easthope_zb":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 创建BeautifulSoup对象
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到所有li标签
        li_tags = soup.find_all('li')

        # 获取最后一个li标签的索引
        last_li_index = len(li_tags) - 1

        # 删除最后一个li标签
        if last_li_index >= 0:
            li_tags[last_li_index].decompose()

        # 查找并删除id为"biddingDocuments"的div标签
        div = soup.find('div', {'id': 'biddingDocuments'})
        div.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "srm_easthope_xj":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(row_value, 'html.parser')

        # 查找并删除id为"biddingDocuments"的div标签
        div = soup.find('div', {'id': 'projectOverview'})
        try:
            div.decompose()
        except Exception as e:
            pass

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "cqggzy_gc" or website == "cqggzy_qt":

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 创建BeautifulSoup对象
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到所有a标签
        a_tags = soup.find_all('a')

        # 删除所有a标签
        for a_tag in a_tags:
            a_tag.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "cdgmgd_wz" or website == 'cdgmgd_zl_g':

        # 获取字段值并转换为字符串类型
        row_value = str(row['x详情页信息'])  # x竞价须知

        # 创建BeautifulSoup对象
        soup = BeautifulSoup(row_value, 'html.parser')

        # 找到所有p标签
        p_tags = soup.find_all('p')

        # 遍历p标签，检查是否有img标签并删除
        for p_tag in p_tags:
            if p_tag.find('img'):
                p_tag.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "portal_ntree_qt":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 选择所有的<th>元素
        th_elements = soup.find_all('th')

        # 修改<th>元素的样式
        for th in th_elements:
            # 获取当前样式属性值
            current_style = th.get('style', '')
            # 添加新的样式
            new_style = current_style + 'min-width:120px;'
            # 更新样式属性
            th['style'] = new_style

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "pangang_zb" or website == "pangang_xj":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 选择所有的 <table> 元素
        table_elements = soup.find_all('table')

        # 修改 <table> 元素的样式
        for table in table_elements:
            # 获取当前样式属性值
            current_style = table.get('style', '')
            # 替换样式
            new_style = current_style.replace('width:100%;', '')
            # 更新样式属性
            table['style'] = new_style

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "bid_xkjt_hw" or website == "bid_xkjt_fw" or website == "bid_xkjt_gc" or website == "bid_xkjt_dy" or website == "bid_xkjt_jj":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 选择所有的元素
        elements = soup.find_all()

        # 移除所有元素的 padding 样式
        for element in elements:
            if 'style' in element.attrs:
                css_styles = element['style'].split(';')
                clean_styles = []
                for style in css_styles:
                    if 'padding' not in style:
                        clean_styles.append(style)
                element['style'] = ';'.join(clean_styles)

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "eps_jiugangbid_xj" or website == "eps_jiugangbid_jj" or website == "eps_jiugangbid_jm":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 选择所有的 <th> 和 <td> 元素
        th_elements = soup.find_all('th')
        td_elements = soup.find_all('td')

        # 给 <th> 元素添加样式
        for th in th_elements:
            th['style'] = 'min-width:120px;' + th.get('style', '')

        # 给 <td> 元素添加样式
        for td in td_elements:
            td['style'] = 'min-width:120px;' + td.get('style', '')

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "e-qyzc":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 找到 HTML 中的最后两个 <tr> 元素
        last_tr_elements = soup.find_all('tr')[-2:]

        # 从 HTML 中删除这两个元素
        for tr in last_tr_elements:
            tr.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "chdtp_dy":

        # 获取字段值并转换为字符串类型
        html = str(row['x基本信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 获取目标元素
        table = soup.find('table')

        # 检查是否找到了目标元素
        if table is None:
            pass
        else:
            # 删除目标元素的 style 属性中的 width 样式
            if 'style' in table.attrs:
                styles = table['style'].split(';')
                updated_styles = [style.strip() for style in styles if not style.lower().startswith('width')]
                table['style'] = ';'.join(updated_styles)

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x基本信息'] = str(soup.prettify())

        return row

    if website == "hnsggzy_cq":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 选择所有的 <th> 和 <td> 元素
        th_elements = soup.find_all('th')

        # 给 <th> 元素添加样式
        for th in th_elements:
            th['style'] = 'min-width:120px;' + th.get('style', '')

        # 找到 HTML 中的最后两个 <tr> 元素
        last_tr_elements = soup.find_all('tr')[-1:]

        # 从 HTML 中删除这两个元素
        for tr in last_tr_elements:
            tr.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "cbex_qt" or website == "cbex_xz" or website == "cbex_sb":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 找到所有的<tr>标签
        tr_tags = soup.find_all('tr')

        # 如果存在倒数第三个<tr>标签，就删除它
        if len(tr_tags) >= 3:
            tr_tags[-3].decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "portal_ntree_sb":

        # 获取字段值并转换为字符串类型
        html = str(row['x标的信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 找到所有的<th>标签
        th_tags = soup.find_all('th')

        # 给每个<th>标签添加min-width:120px样式属性
        for th in th_tags:
            th['style'] = 'min-width:120px;' + th.get('style', '')

        # 将修改后的 HTML 代码放回原始数据中
        dfs.at[_, 'x标的信息'] = str(soup.prettify())

        # 获取字段值并转换为字符串类型
        html = str(row['x交易条件'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 找到所有的<th>标签
        th_tags = soup.find_all('th')

        # 给每个<th>标签添加min-width:120px样式属性
        for th in th_tags:
            th['style'] = 'min-width:120px;' + th.get('style', '')

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x交易条件'] = str(soup.prettify())

        return row

    if website == "ljqrmyy_gs":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 查找所有具有特定类的元素
        pf_divs = soup.find_all('div', class_='pf')

        # 遍历每个元素并删除
        for div in pf_divs:
            div.decompose()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "szecp_xwz" or website == "szecp_cg" or website == "szecp_zb" or website == "dyggzy_gz":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 查找所有具有特定类的元素
        p_stories = soup.find_all('p', class_='story')

        # 遍历每个元素并设置边距为 0
        for story in p_stories:
            story['style'] = 'margin: 0;'

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    # 12-15
    if website == "wfjztb_kdcloud_cg":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        soup = BeautifulSoup(html, 'lxml')

        # 遍历所有元素
        for element in soup.find_all():
            # 检查元素是否有style属性
            if 'style' in element.attrs:
                # 获取当前style属性的值
                style = element['style']

                # 使用正则表达式删除所有关于padding的属性
                style = re.compile(r'padding:\s*[\d\.]+(?:px)?;?', re.I).sub('', style)

                # 更新元素的style属性
                element['style'] = style

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    if website == "eps_dhidcw_zb" or website == "eps_dhidcw_cg":

        # 获取字段值并转换为字符串类型
        html = str(row['x详情页信息'])  # x竞价须知

        # 假设html文档已经读入到了变量html_doc中
        soup = BeautifulSoup(html, 'html.parser')

        # 查找所有的div元素
        for div in soup.find_all('div'):
            # 查找div下一级的a标签
            for a in div.find_all('a', recursive=False):
                # 如果a标签的文本是"返回"，则删除这个div元素
                if a.string == "返回":
                    div.extract()

        # 将修改后的 HTML 代码放回原始数据中
        row.at['x详情页信息'] = str(soup.prettify())

        return row

    return row
