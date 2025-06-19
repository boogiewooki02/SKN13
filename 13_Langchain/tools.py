# tavily_search를 이용해서 web 검색을 처리하는 툴
from typing import Literal # 넣을 수 있는 값이 정해진 경우 사용
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_community.document_loaders import WikipediaLoader
from langchain_core.runnables import chain
from pydantic import BaseModel, Field


@tool
def search_web(query: str, 
               max_results: int=3, 
               time_range: Literal["day", "week", "month", "year"]|None=None) -> dict:
    """
    데이터베이스에 존재하지 않는 정보나 최신 정보를 찾기 위해서 인터넷 검색을 하는 Tool입니다.

    """
    tavily_search = TavilySearch(max_results=max_results, time_range=time_range)
    search_result = tavily_search.invoke(query)["results"] # {..., "results": list[dict]}
    if search_result:
        return {"result": search_result}
    else:
        return {"result": "검색 결과가 없습니다."}
    

@chain
def wikipedia_search(input_dict: dict) -> dict:
    """사용자 query에 대한 정보를 위키백과사전에서 k개의 문서를 검색하는 Runnable"""

    query = input_dict['query'] # 검색어
    max_results = input_dict.get('max_results', 2) # 조회 문서 최대 개수

    wiki_loader = WikipediaLoader(query=query, load_max_docs=max_results, lang='ko')
    search_result = wiki_loader.load() # list[Documnet]
    if search_result: # 검색 결과가 있다면
        result_list = []
        for doc in search_result:
            result_list.append({"content": doc.page_content, "url": doc.metadata['source'], "title": doc.metadata['title']})
        return {"result": result_list}
    else:
        return {"result": "검색 결과가 없습니다."}
    

# Runnable을 tool로 - runnable.as_tool(툴 정보)
class SearchWikiArgsSchema(BaseModel):
    query: str = Field(..., description="위키백과사전에서 검색할 키워드, 검색어")
    max_results: int = Field(default=2, description="검색할 문서의 최대 개수")

search_wiki = wikipedia_search.as_tool(
    name="search_wikipedia",
    description=("위키 백과사전에서 정보를 검색할 때 사용하는 tool.\n"
                 "사용자의 질문과 관련된 위키백과사전의 문서를 지정한 개수만큼 검색해서 반환합니다.\n"
                 "일반적인 지식이나 배경 정보가 필요한 경우 유용하게 사용할 수 있는 tool입니다."),
    args_schema=SearchWikiArgsSchema # 파라미터(argument)에 대한 설계
)
