# 라라벨 믹스 (Laravel Mix)

- [소개](#introduction)

<a name="introduction"></a>
## 소개

> [!WARNING]
> 라라벨 믹스는 현재 더 이상 활발히 유지 관리되지 않는 레거시 패키지입니다. 최신 대안으로 [Vite](/docs/master/vite)를 사용할 수 있습니다.

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com)를 만든 Jeffrey Way가 개발한 패키지로, 여러 가지 일반적인 CSS 및 JavaScript 전처리기를 활용하여 라라벨 애플리케이션의 [webpack](https://webpack.js.org) 빌드 단계를 정의할 수 있는 유연한 API를 제공합니다.

즉, Mix는 애플리케이션의 CSS와 JavaScript 파일을 쉽게 컴파일하고 축소(minify)할 수 있도록 도와줍니다. 간단한 메서드 체이닝을 통해 에셋 파이프라인을 쉽게 정의할 수 있습니다. 예를 들어 다음과 같이 사용할 수 있습니다.

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

webpack과 에셋 컴파일을 시작하려고 할 때 막막함이나 혼란을 느껴본 적이 있다면, Laravel Mix가 큰 도움이 될 것입니다. 하지만 애플리케이션 개발 시 반드시 Mix를 사용해야 하는 것은 아니며, 원하는 에셋 파이프라인 도구를 자유롭게 사용할 수 있고, 아예 사용하지 않아도 무방합니다.

> [!NOTE]
> 새로운 라라벨 설치에서는 Vite가 Laravel Mix를 대체하고 있습니다. Mix에 관한 공식 문서는 [Laravel Mix 공식 사이트](https://laravel-mix.com/)에서 확인할 수 있습니다. Vite로 이전하고자 한다면, [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하시기 바랍니다.
