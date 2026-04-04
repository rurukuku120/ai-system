# VFX 평가 요청 방법

이 폴더에 스크린샷을 올리면 자동으로 평가가 실행됩니다.

## 파일 업로드 방법

### GitHub 웹에서 (Git 설치 불필요)
1. [inbox 폴더](.) 접속
2. 우측 상단 **Add file → Upload files** 클릭
3. 스크린샷 파일 드래그 & 드롭
4. **Commit changes** 클릭

### 파일명 규칙
```
작업명_작업자_스킬유형.png
```
예시:
```
소드슬래시히트_홍길동_히트이펙트.png
파이어볼AOE_김철수_AOE.png
보스등장연출_이영희_보스패턴.png
```

스킬유형 목록: `히트이펙트` / `AOE` / `버프` / `보스패턴` / `기타`

## 자동 실행 내용

파일 업로드 후 약 1~2분 내 자동으로:
1. Claude AI가 6개 항목 평가 (1~5점)
2. `results/` 폴더에 JSON 저장
3. Notion VFX 피드백 DB에 등록

## 결과 확인

- **Git**: `projects/nexon/mabinogi-eternity/evaluations/results/`
- **Notion**: VFX 피드백 데이터베이스
