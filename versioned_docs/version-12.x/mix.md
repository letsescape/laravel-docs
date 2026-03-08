# Laravel Mix

- [소개](#introduction)

<a name="introduction"></a>
## 소개

> [!WARNING]
> Laravel Mix는 더 이상 활발하게 유지 관리되지 않는 레거시 패키지입니다. 현대적인 대안으로 [Vite](/docs/12.x/vite)를 사용할 수 있습니다.

[Laravel Mix](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com) 제작자 제프리 웨이가 개발한 패키지로, Laravel 애플리케이션에서 여러 일반적인 CSS 및 JavaScript 전처리기들을 사용하여 [webpack](https://webpack.js.org) 빌드 단계를 정의할 수 있는 직관적인 API를 제공합니다.

즉, Mix는 애플리케이션의 CSS와 JavaScript 파일을 컴파일하고 압축하는 작업을 매우 쉽게 만들어 줍니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 자연스럽게 정의할 수 있습니다. 예를 들어:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');
```

만약 webpack과 자산 컴파일을 시작하는 과정에서 혼란스럽고 어려움을 느꼈다면 Laravel Mix가 매우 유용할 것입니다. 그러나 애플리케이션 개발 시 반드시 Mix를 사용해야 하는 것은 아니며, 원하는 어떤 자산 파이프라인 도구든지, 또는 아예 사용하지 않아도 자유롭게 선택할 수 있습니다.

> [!NOTE]
> Vite는 새로운 Laravel 설치 환경에서 Laravel Mix를 대체하고 있습니다. Mix 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트를 참고하세요. Vite로 전환하려면 [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하시기 바랍니다.