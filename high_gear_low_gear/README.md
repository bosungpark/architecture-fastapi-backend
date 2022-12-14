**LOW GEAR AND HIGH GEAR**

*하이레벨? 로우레벨? 어떤 테스트를 작성해야 하는가?*

- 로우 레벨의 유닛테스트가 너무 많다면, 코드의 변경이 있을 때마다 테스트는 쉽게 깨지곤 한다.


- 만일 하이 레벨의 테스트(세비스 레이어)가 정교하게 구성되었다면, 도메인 단의 테스트는 비교적 신경쓰지 않아도 된다.


- 단, 유닛 테스트가 필요없다는 의미는 아니다. e2e 테스트는 적은 코드로도 커버리지가 높은 대신 낮은 피드백과 변화에 대한 감지를 제공한다.


- 또 적절하게 작성된 테스트 코드는 전체적인 시스템과 모델에 대한 가이드가 되어줄 수 있다. 새로운 멤버가 잘 작성된 테스트코드를 본다면 프로젝트에 대해 빠르게 파악할 수 있을것이다.

*하이기어와 로우기어*

- 대부분의 경우, 피쳐를 개발하거나 버그 픽스를 하더라도 도메인 모델을 많이 수정하지는 않는다. 이런 경우라면 서비스 레이어를 테스트하는 것이 유리하다. 왜냐하면 결합도를 낮출 수 있고, 높은 커버리지를 가지기 때문이다.


- 하지만 만약 새롭거나, 기막힌 프로젝트를 해야 한다면, 도메인 부터 시작하는 것이 좋다. 더 섬세한 피드백을 받을 수 있고, 의도에 맞는지 여부를 쉽게 파악할 수 있기 때문이다.


- 기어는 이에 대한 비유이다. 자전거를 탈 때, 처음에는 로우기어를 사용하고 이후 기어를 올리듯이 테스트코드를 작성할 때에도 적절한 전략을 선택하는 것을 말한다. 개발초기에는 조금 느리지만 안전한 방식을, 속도가 붙으면 효율적인 방식을 사용해 개발을 하는 것을 권장한다.

