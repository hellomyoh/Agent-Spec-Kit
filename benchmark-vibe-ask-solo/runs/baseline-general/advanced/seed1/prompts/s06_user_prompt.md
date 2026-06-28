# advanced S6 - user prompt

의도적 변경(S3 안전 정책상 현재 blank query가 []를 반환하는 걸 알고 있음): 새 목록 뷰를 위해 이제 blank query는 전체 아이템을 반환하도록 한다. S3 blank 정책을 supersede하고 문서/테스트를 갱신하되, where/sort/limit/unknown-field 동작은 그대로 유지해줘.
