from typing import List, Dict, Optional

#########################################
# TYPING                                #
#########################################
Coauthors = Optional[List[Dict[str, str]]]


#########################################
# VALIDATION                            #
#########################################
APPLICATION_ROLES = ("студент", "аспирант", "сотрудник")
RE_LINE_ID = r"^\d+$"
RE_LINE_FIO = r"^(?:[А-Я]|[а-я]|-)+$"
RE_LINE_ADVISER = r"^(?:[А-Я]|[а-я]|-|.)+$"