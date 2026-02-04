# 🖥️ 세팅 대시보드

### 사내 PC 세팅 업무를 한눈에 관리하고 자동화하기 위한 내부 웹 대시보드

복잡한 세팅 단계와 흩어진 정보를 하나의 화면으로 정리하고,  
반복적인 외부 작업을 버튼 클릭으로 간소화해요.

<img width="800" height="473" alt="image" src="https://github.com/user-attachments/assets/e656df5c-542e-44c1-84e6-83ffe12d17a7" />

<br/>
<br/>

## 📌 프로젝트 정보

- **웹 기반 내부 세팅 대시보드**
  - 직원 PC 세팅을 담당하는 팀 내부에서 사용하는 도구
- **단기 계약직 근무 당시, 팀원 요청으로 혼자 개발**
  - 디자인: 팀원
  - 프론트엔드 / 백엔드 등 개발 담당
- 포트폴리오 용도로 개인적으로 재구현한 프로젝트

<br/>

## 🧩 프로젝트 주제

- **사내 PC 세팅 업무 자동화 및 현황 관리 대시보드**
  - 신규 입사 / 교체 / 복직 / 전환 시 필요한 PC 세팅 관리
  - 여러 문서와 툴에 분산된 정보를 하나의 화면으로 통합
  - 외부 서비스(Okta, Slack 등) 작업을 대시보드에서 바로 처리

<br/>

## 💡 프로젝트 기획 의도

PC 세팅 담당 팀의 업무는 **단계가 많고, 확인해야 할 정보가 분산되어 있어 작업 피로도가 높았습니다.**

- 기존 문제점
  - 슬랙 채널, 문서, 엑셀 등을 동시에 확인해야 함
  - 세팅 단계가 복잡해 현재 상태 파악이 어려움
  - Okta, Slack 등 외부 서비스 작업을 직접 오가며 처리해야 함

- 해결 목표
  - **세팅 현황을 한눈에 볼 수 있는 대시보드 제공**
  - 반복적인 외부 작업을 버튼 클릭으로 단순화
  - 수동 입력을 최소화하기 위한 자동 데이터 수집

<br/>

## 🛠️ 개발 환경

### 기술 스택

<div style="overflow-x:auto;">
<table style="width: 100%; border-collapse: collapse;">
  <tr>
    <td style="padding: 10px;">Backend</td>
    <td style="padding: 10px;">
        <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white" />
        <img src="https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white" />
        <img src="https://img.shields.io/badge/Bolt-611f69?style=flat&logo=slack&logoColor=white" />
    </td>
  </tr>
  <tr>
    <td style="padding: 10px;">Workflow / Scheduler</td>
    <td style="padding: 10px;">
        <img src="https://img.shields.io/badge/Apache%20Airflow-017CEE?style=flat&logo=Apache%20Airflow&logoColor=white"/>
    </td>
  </tr>
  <tr>
    <td style="padding: 10px;">DB</td>
    <td style="padding: 10px;">
        <img src="https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=flat&logo=mongodb&logoColor=white" />
    </td>
  </tr>
  <tr>
    <td style="padding: 10px;">External Services</td>
    <td style="padding: 10px;">
        <img src="https://img.shields.io/badge/Okta-007DC1?style=flat&logo=okta&logoColor=white"/>
        <img src="https://img.shields.io/badge/Slack-4A154B?style=flat&logo=slack&logoColor=white"/>
        <img src="https://img.shields.io/badge/Kandji-000000?style=flat&logo=&logoColor=white"/>
        <img src="https://img.shields.io/badge/Intune-0078D4?style=flat&logo=microsoft&logoColor=white"/>
    </td>
  </tr>
  <tr>
    <td style="padding: 10px;">Tools</td>
    <td style="padding: 10px;">
        <img src="https://img.shields.io/badge/Github-181717?style=flat&logo=github&logoColor=white"/>
        <img src="https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=Postman&logoColor=white"/>
    </td>
  </tr>
</table>
</div>

<br/>

## ✨ 핵심 기능


### 📋 세팅 데이터 관리

- 세팅 수동 생성
- 전체 조회
  - 검색
  - 필터링
- 상세 패널을 통한 개별 관리
- 세팅 수정
  - 세팅 정보
  - 체크리스트
  - 메모
  - 상태
- 수동 생성 데이터 삭제 가능

|               세팅 생성               |            **검색 및 필터링**             |
| :-----------------------------------: | :-----------------------------------: |
| <img width="400" height="225" src="https://github.com/user-attachments/assets/93f5e5ae-c46e-4e68-a98e-13310c258984"> | <img width="400" height="225" src="https://github.com/user-attachments/assets/10231a5e-c535-43c4-b584-c9d7b8761b80"> |
|       **개별 조회**       |          **세팅 삭제**           |
| <img width="400" height="225" src="https://github.com/user-attachments/assets/f165ff8f-41fd-4eac-a962-48f35a97ad21"> | <img width="400" height="225" src="https://github.com/user-attachments/assets/e485938a-35a3-4cd3-9972-6292f398620f"> |
|             **개인정보 수정**             |            **체크리스트 수정**            |
| <img width="400" height="225" src="https://github.com/user-attachments/assets/768f1f9d-7e40-4d1f-8554-aaa1b5e68ddf"> | <img width="400" height="225" src="https://github.com/user-attachments/assets/f447884c-858a-4c31-ace0-42cb24f397fd"> |
|             **메모 수정**             |             **상태 수정**             |
| <img width="400" height="225" src="https://github.com/user-attachments/assets/f488476f-0f81-4595-89c7-151d108f3eda"> | <img width="400" height="225" src="https://github.com/user-attachments/assets/855cd31a-7f99-4403-bd12-9df57ab8b674"> |

<br/>

### ⚡ 빠른 작업 (외부 서비스 연동)

- 대시보드 버튼 클릭으로 외부 작업 처리
- 반복적인 외부 서비스 이동 최소화

**지원 기능**

- Okta
  - 세팅 그룹 할당
  - 비밀번호 초기화
  - 계정 활성화 (복직자)
- Slack
  - 비밀번호 초기화 안내 DM
  - 장비 수령 안내 DM

|         개별 빠른 작업         |          Slack DM 전송 결과           |
| :-----------------------------------: | :-----------------------------------: |
| <img width="400" height="225" src="https://github.com/user-attachments/assets/fbc65959-4b7e-43f5-a1e9-8867e46ed4e2"> | <img width="400" height="225" src="https://github.com/user-attachments/assets/c1949088-147d-4d27-8f55-940375826171"> |

<br/>


### 📦 일괄 작업

- 체크박스를 이용한 다중 선택
- 선택한 세팅 데이터 일괄 처리
  - 정보 수정
  - 빠른 작업 실행

|            일괄 정보 수정             |            일괄 빠른 작업             |
| :-----------------------------------: | :-----------------------------------: |
| <img width="400" height="225" src="https://github.com/user-attachments/assets/b7a797ad-8ac8-41a1-b54f-1ea2a84044d3"> | <img width="400" height="225" src="https://github.com/user-attachments/assets/d3580d88-5624-46ab-a4d6-e4a9c028270f"> |
|       **선택 데이터 확인 모달**       |
| <img width="400" height="225" src="https://github.com/user-attachments/assets/70873242-e98d-4104-bf38-5cc531b90675"> |

<br/>


### 🔄 자동 데이터 수집

- 기존 PC 자산 조회 시스템과 연동
- Kandji / Intune을 통해 출고 상태 확인
- Apache Airflow 배치 처리
  - 출고 완료 시 세팅 대시보드에 자동 추가
- 수동 데이터 입력 최소화

