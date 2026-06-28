# advanced S5 - user prompt

의도적 변경: 모든 아이템에 없는 where 키는 이제 raise하지 말고 무시하여 `[]`를 반환한다(ValueError 폐기). 명세/테스트를 그에 맞게 갱신하고, 나머지 정책은 그대로.
