from os.path import join as join_path, abspath, dirname
import dawg, re

def string_full2half(string):
    """全角字符串转半角"""
    def full2half(char):
        """全角字符转半角"""
        code = ord(char)
        if code == 12288: #空格要特殊处理
            return chr(32)
        if 65281<=code<=65374:
            return chr(code-65248)
        return char
    return ''.join(map(full2half, list(string)))

class NormCompany:
    def __init__(self):
        model_path = join_path(abspath(dirname(__file__)), '../../data/kg/')
        file = open(model_path + "location.txt").read().split("\n")
        self.city = {}

        for c in file:
            items = c.split(",")
            if len(items) > 1:
                self.city[items[1]] = items[0]
        self.location = set(list(self.city.keys()) + list(self.city.values()))
        self.sub_postfix = {
            "分公司", "第一分公司", "第二分公司", "办事处", "代表处", "分社", "分行", "分店", "分部", "分中心", "分院", "分所", "联络处",
            "商务处", "中心支公司", "二公司"
        }
        self.company_postfix = {
            "有限公司", "股份有限公司", "有限责任公司", "控股股份有限公司", "控股有限公司", "控股有限公司", '控股有限责任公司', '控股公司',
            "发展(集团)有限公司", "普通合伙", "合伙企业(有限合伙)", "(普通合伙)", "(特殊普通合伙)", "特殊普通合伙", "(个人独资)",
            '有限公司', "(控股)有限公司", '股份公司', '集团公司', '发展控股集团有限公司', '(集团)公司', '总公司', "公司", "集团有限责任公司",
            "企业股份有限公司", "股份有限公司", "集团有限公司", "发展有限责任公司", "集团有限责任公司", "(公司)", "(集团)有限责任公司",
            "集团股份有限公司", '(集团)股份有限公司', '(集团)有限公司', '(集团)有限责任公司', '控股集团', "集团", "控股集团有限公司",
            "发展股份有限公司", "发展控股有限公司", "发展公司", "集团控股有限公司", "合伙企业(普通合伙)", "(有限责任公司)",
            "控股集团股份有限公司", "(有限合伙)", "有限合伙企业", "合伙企业", "有限合伙", "发展有限公司", "(控股)集团", "(有限合伙企业)",
            "(集团)", "发展集团有限公司", "企业集团有限公司", "(有限公司)", "(微型企业)", "有限公司(微型企业)", "有限责任公司(微型企业)",
            "(集团)实业有限公司", "(集团)总公司", "(股份)有限公司"
        }
        self.bug_word = {"政", "建"}
        self.bracket = {"(", ")", "[", "]", "{", "}"}
        self.pat_alnum = re.compile(r'^[a-zA-Z0-9]+$')
        file = open(model_path + "industry_company_itjuzi.txt", "r").read().split("\n")
        self.all_postfix = self.company_postfix | self.sub_postfix
        n = 0
        self.tags = set()
        while n < len(file):
            if n:
                items = file[n].split("\t")
                if items[0]:
                    self.tags.add(items[0])

            n += 1
        self.all_policy = self.company_postfix | self.sub_postfix | self.location | self.bracket | self.tags
        self.trie = dawg.CompletionDAWG(list(self.all_policy))

        industry_relation = open(model_path + "norm_industry.txt").read().split("\n")
        self.encoder = {}
        self.decoder = {}
        n = 1
        for idr in industry_relation:
            if not idr:
                continue
            items = idr.split("\t")
            tags = sorted(items[1].split("|"))
            self.decoder[tuple(tags)] = items[0]
            for t in tags:
                if t not in self.encoder.keys():
                    self.encoder[t] = []
                self.encoder[t].append(n)
            n += 1
        self.location_trie = dawg.CompletionDAWG(self.location)

    def get_real_industry(self, industries):
        codes = {}
        for ids in industries:
            for tag in self.encoder.get(ids, []):
                if tag not in codes:
                    codes[tag] = []
                codes[tag].append(ids)
        result = set(industries)
        for co in codes.values():
            result.add(self.decoder.get(tuple(sorted(co)), ""))
        clean_result = list(filter(lambda x: x, result))
        return clean_result

    def longest_prefix_(self, line):
        '''返回最长前缀对应的token'''
        w = ''
        for w in sorted(self.trie.prefixes(line), key=lambda x: len(x), reverse=True):
            if len(w) > 1 and len("".join(self.trie.prefixes(line[len(w) - 1:len(line)]))) > 1:
                continue
            return w

    def longest_prefix(self, line):
        '''返回最长前缀对应的token'''
        w = ''
        for w in sorted(self.trie.prefixes(line), key=lambda x: len(x), reverse=True):
            if len(w) > 1 and len("".join(self.trie.prefixes(line[len(w) - 1:len(line)]))) > 1:
                continue
            return w

    def get_cut_section(self, s):  # 当字符串非关键词时，获取字符串中的关键词，具体：获取以首字符为前缀，如果有，获取前缀最长的，如果没，先后移
        if isinstance(s, str):
            length = len(s)
            n = 0
            kw = []
            name = ""
            while n < length:
                trie_words = self.longest_prefix(s[n:length])
                if trie_words:
                    if name:
                        kw.append(name)
                        name = ""
                    kw.append(trie_words)
                    n += len(trie_words)
                else:
                    name += s[n]
                    n += 1
            if name:
                kw.append(name)
            return list(kw)
        else:
            return []

    def get_policy_name(self, s):
        result = {"location": [], "alias": [], "postfix": [], "sub_postfix": [], "industry": []}
        sub_postfix = ""
        # non_alias = ""
        section = self.get_cut_section(s)
        i = 0
        while i < len(section):
            word = section[i]
            if word in ["", " ", "   ", ' ']:
                pass
            elif result.get("postfix", []) or sub_postfix:

                sub_postfix += word
            elif word not in self.all_policy:
                result["alias"].append(word)
            # non_alias += word

            elif word in self.company_postfix:
                if i < len(section) - 1 and section[i + 1] in self.tags and section[
                    len(section) - 1] in self.company_postfix:
                    result["alias"].append(word)
                    result["industry"].append(word + section[i + 1])
                    i += 1
                else:
                    result["postfix"].append(word)
            elif word in self.sub_postfix:
                sub_postfix += word
            elif word in self.bracket:
                if i < len(section) - 1 and section[i + 1] not in self.all_policy:
                    result["alias"].append(word)
            elif word in self.location:
                if i == 0:
                    if i < len(section) - 1 and section[i + 1] in self.all_postfix | self.tags:
                        result["alias"].append(word + section[i + 1])
                        # non_alias += word + section[i + 1]

                        i += 1
                    elif word in self.city.keys() and i < len(section) - 1 and section[i + 1] in self.bug_word:
                        result["location"].append(word[0:len(word) - 1])
                        result["alias"].append(word[len(word) - 1] + section[i + 1])
                        # non_alias += word[len(word) - 1] + section[i + 1]
                        i += 1
                    else:
                        result["location"].append(word)

                elif i < len(section) - 1 and section[i - 1] in self.bracket and section[i + 1] in self.bracket:
                    if result["location"] and not (result["alias"]):
                        result["alias"].append(result["location"][0])
                    # non_alias += result["location"][0]
                    result["location"] = [section[i - 1] + word + section[i + 1]]
                    i += 1

                elif i < len(section) - 1 and section[i + 1] in self.sub_postfix:
                    sub_postfix += word + section[i + 1]
                    i += 1

                elif word in self.city.keys():
                    result["location"].append(word)

                elif len("".join(result.get("alias", []))) < 2:
                    result["alias"].append(word)
                # non_alias += word

                elif len(section) - 1 > i and section[i + 1] in self.all_postfix:
                    result["location"].append(word)

                elif i == len(section) - 1:
                    result["location"].append(word)
                else:
                    result["alias"].append(word)
                # non_alias += word

            elif len("".join(result.get("alias", []))) > 1 and word in self.tags:
                if len(section) - 1 > i and section[i + 1] not in self.all_policy:
                    result["alias"].append(word + section[i + 1])
                    # non_alias += word + section[i + 1]

                    i += 1
                else:
                    result["industry"].append(word)
            else:
                result["alias"].append(word)
            # non_alias += word

            i += 1

        if sub_postfix:
            result["sub_postfix"].append(sub_postfix)
        return result

    def norm_city(self, s):
        city = s
        bracket = set(city) & self.bracket
        for b in bracket:
            city = city.replace(b, "")
        if city in self.city.keys():
            return self.city[city]
        elif city in self.city.values():
            return city
        return s

    def get_norm_name(self, s):
        if not isinstance(s, str):
            return s, None
        name = string_full2half(s).strip()
        section = self.get_policy_name(name)
        postfix = section.get("postfix", []) + section.get("sub_postfix", [])

        if len("".join(section.get("alias", []))) < 2:
            for kw in postfix:
                name = name.replace(kw, "")
        else:
            for kw in postfix + section.get("location"):
                name = name.replace(kw, "")
        cities = []
        for c in section.get("location"):
            cities.append(self.norm_city(c))
        if len(name) < 2:
            return s, []
        elif len(name) == 2 and "控股" in "".join(section.get("postfix")):
            name = name + "控股"
        elif name in self.tags | self.location:
            return s, []
        return name, cities

    def get_origin_base_info(self, s):
        policy = self.get_policy_name(s)
        result = {
            "base_location": "".join(map(lambda x: self.norm_city(x), policy.get("location", []))),
            "base_alias": "".join(policy.get("alias", [])),
            "base_industry": policy.get("industry", []),
            "base_postfix": "".join(policy.get("postfix", [])),
            "base_sub_postfix": "".join(policy.get("sub_postfix", []))
        }
        return result

    def get_base_info(self, s):
        policy = self.get_policy_name(s)
        sub_location = list(
            filter(lambda x: x in self.location, self.get_cut_section("".join(policy.get("sub_postfix", [])))))
        if sub_location:
            sub_location = self.norm_city(sub_location[0])
        else:
            sub_location = ""
        result = {
            "base_location": "".join(map(lambda x: self.norm_city(x), policy.get("location", []))),
            "base_alias": "".join(policy.get("alias", [])),
            "base_industry": self.get_real_industry(policy.get("industry", [])),
            "base_postfix": "".join(policy.get("postfix", [])),
            "base_sub_postfix": "".join(policy.get("sub_postfix", [])),
            "sub_location": sub_location
        }
        return result


norm_company = NormCompany()

if __name__ == "__main__":
    for i in [
        "索尼(中国)有限公司 济南分公司", "上海有限公司", "东方集团股份有限公司", "深圳市龙岗分公司", "成都市政公司",
        "达内时代科技集团有限公司北京第十二分公司", "达内时代科技集团有限公司北京分公司", [], "中国建设银行公司",
        "美国福陆(中国)工程建设有限公司", "广东岭南通股份有限公司", "佛山市集成金融集团有限公司",
        "江苏省徐州市世通重工机械制造有限责任公司", "惠州百度分公司", "唐山湾（上海）投资控股有限公司", "安国(深圳)有限公司",
        "内蒙古鄂尔多斯投资控股有限公司", "国安达股份有限公司", "巴中国联秦巴电子商务有限公司", "随身云南京信息技术有限公司",
        "腾讯电子商务上海有限公司", "合肥天焱生物质能科技有限公司青岛分公司", "技术投资(厦门)网络科技有限公司",
        "中汇会计师事务所（特殊普通合伙）", "新东方教育科技集团合肥学校", "北京市太极无人飞机有限公司", "国际商业机器（中国）有限公司",
        "车音智能有限公司北京分公司", "北京建工集团有限责任公司国际工程部", "中国移动通信集团重庆有限公司"
    ]:
        print(i, norm_company.get_base_info(string_full2half(i)))
# print(norm_company.get_cut_section(i))
