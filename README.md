# SKN09-4th-3Team

**SK네트웍스 Family AI 캠프 9기 4차 프로젝트**

# 1. 팀 소개
  ### 팀명:LLM(Lending Loan Mentor)
<br>

### 💲팀원 소개
><table align=center>
>  <tbody>
>    <br>
>      <td align=center><b>서예찬</b></td>
>      <td align=center><b>전성원</b></td>
>     <td align=center><b>조민훈</b></td>
>      <td align=center><b>최재동</b></td>
>    </tr>
>    <tr>
>      
>    
>    </tr>
>    <tr>
>      <td><a href="https://github.com/syc9811"><div align=center>@syc9811</div></a></td>
>      <td><a href="https://github.com/Hack012"><div align=center>@Hack012</div></a></td>
>      <td><a href="https://github.com/alche22"><div align=center>@alche22</div></a></td>
>      <td><a href="https://github.com/Monkakaka"><div align=center>@Monkakaka</div></a></td>
>    </tr>
>  </tbody>
></table>
><br>

# 2. 프로젝트 개요

### 💲프로젝트 명
- LLM 기반 대출관련 챗봇 시스템

### 💲프로젝트 소개
> **“당신에게 맞는 대출, AI와 함께 쉽고 정확하게 찾으세요.”**

**Team LLM의 대출 챗봇 시스템**은 대형 언어 모델(LLM)을 활용해 사용자의 금융 질문에 실시간, 맞춤형 상담을 제공하는 AI 기반 금융 전문가 입니다.<br>
은행별 상이한 대출 조건과 잦은 정책 변경으로 인한 금융 정보 격차 문제를 해소하고, 보다 합리적인 대출 의사결정을 돕는 것이 목표로 가집니다.

<pre>  <b>주요 기능</b>

    ✅ 최신 정책 반영 기반의 대출 조건 안내  <br>
    ✅ 주택 보유 상태·대출 목적 등 사용자 상황에 따른 상품 추천  <br>
    ✅ 대출 상환 계획 계산기 탑재 (이자 계산 및 상환 시뮬레이션)  <br>
    ✅ 직관적 UI로 누구나 쉽게 사용 가능 (금융 취약 계층 고려)  <br>
    ✅ RAG 기반 신뢰도 높은 데이터 응답 + 계산 특화 LLM 연동  <br>
</pre>

### 💲프로젝트 필요성 (배경)
<div align="center">
  <img src="https://github.com/user-attachments/assets/38724149-d141-4b31-ac2a-e9316a74091c" width="45%" />
  <img src="https://github.com/user-attachments/assets/e05cb257-4bf1-48b2-b828-982d8af33675" width="45%" />
</div>

- 최근 강남3구(강남·서초·송파)와 용산구가 토지거래 허가구역으로 지정되면서, KB국민·신한·하나·우리·NH농협 등 주요 은행들이 각기 다른 대출 기준과 절차를 운영 이에 따라 대출 신청 시 필요한 서류, 한도, 금리 등이 은행별로 상이하며, 일부 은행은 신규 주택 취득 목적 대출만 허용하거나, 보유 주택의 전세자금대출을 제한하는 등 정책 차이가 발생하고 있음.
- 각 은행의 대출 정책이 자주 변동되고, 지역 및 주택 보유 수에 따른 대출 규제가 수시로 변경되면서 소비자들이 자신에게 적합한 대출 상품을 찾기가 점점 어려워지는 상황.
- 특히, 일부 지역에서는 매입 목적, 전세자금 여부, 기존 주택 보유 상태에 따라 대출 가능 여부가 달라지기 때문에, 정확한 정보를 확보하지 못하면 잘못된 금융 의사결정을 내릴 위험이 다분함.

🔗 **출처**
- https://news.nate.com/view/20250323n17586
- https://www.yna.co.kr/view/AKR20250322045500002?section=popup

### 💲프로젝트 목표
- **목표**: 사용자에게 대출 상품에 대한 상담, 신청 조건 안내, 상환 계획 계산 등 금융 관련 질문에 실시간으로 답변을 제공하는 것.

<br>


# 3. 기술 스택

| 분야                   | 기술 및 라이브러리                                                                                                                                                                                                                                       |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 프로그래밍 언어 & 개발환경 | <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white" /> <img src="https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=https://gist.githubusercontent.com/yourusername/uniqueid/raw/vscode-logo.svg&logoColor=white" /> <img src="https://img.shields.io/badge/Jupyter-%23FA0F00.svg?style=for-the-badge&logo=Jupyter&logoColor=white" /> |
| 웹 프레임워크            |                                                                                                                                |
| LLM 체인 및 자연어 처리   |![LangChain](https://img.shields.io/badge/LangChain-005F73?style=for-the-badge&logo=LangChain&logoColor=white)                                                                                                     |
| AI 모델               |  <img src="https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=HuggingFace&logoColor=black" />                         |
| 데이터베이스 및 임베딩     |                                                                                                  |
| 환경변수 관리            | <img src="https://img.shields.io/badge/python_dotenv-000000?style=for-the-badge&logo=Python&logoColor=white" />                                                                                                                                      |
| 문서 로딩               | <img src="https://img.shields.io/badge/PyPDFLoader-4B8BBE?style=for-the-badge&logo=PyPDFLoader&logoColor=white" />                                                                                                                                              |
| 협업 및 형상관리        | <img src="https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=Discord&logoColor=white" /> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white" /> <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white" /> |

<br>

# 4. 시스템 구성도
![Image](https://github.com/user-attachments/assets/305b7de7-4d23-4c81-a723-70e5b8a05316)

# 5. 요구사항 정의서 (캡처)
# 6. 화면설계서 (캡처)
# 7. WBS
# 8. 테스트 계획 및 결과 보고서 (캡처)
# 9. 수행결과(테스트/시연 페이지)
# 10. 한 줄 회고
💰 서예찬
💰 전성원 
💰 조민훈
💰 최재동
