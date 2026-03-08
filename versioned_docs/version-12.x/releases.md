# 릴리즈 노트 (Release Notes)

- [버전 관리 정책](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 정책 (Versioning Scheme)

Laravel과 주요 1차 제공 패키지들은 [시맨틱 버전 관리(Semantic Versioning)](https://semver.org)을 따릅니다. 주요 프레임워크 릴리즈는 매년(대략 1분기)에 출시되며, 마이너 및 패치 릴리즈는 매주 출시될 수 있습니다. 마이너 및 패치 릴리즈에는 절대로 **호환성이 깨지는 변경사항**이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 및 컴포넌트를 참조할 때는 반드시 `^12.0`과 같은 버전 제약 조건을 사용하시기 바랍니다. Laravel의 주요 릴리즈에는 호환성이 깨지는 변경 사항이 포함될 수 있기 때문입니다. 그러나, 새로운 주요 릴리즈로 하루 이내에 업그레이드할 수 있도록 항상 최선을 다하고 있습니다.

<a name="named-arguments"></a>
#### 네임드 인수 (Named Arguments)

[네임드 인수(named arguments)](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 정책에 포함되지 않습니다. 필요에 따라 Laravel 코드베이스 개선을 위해 함수 인수명을 변경할 수 있습니다. 따라서, Laravel 메서드를 호출할 때 네임드 인수를 사용할 경우 인수명이 향후 변경될 수 있음을 유념하시고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리즈는 버그 수정이 18개월, 보안 수정이 2년 동안 제공됩니다. 추가 라이브러리의 경우, 오직 최신 주요 릴리즈만 버그 수정을 받습니다. 또한, Laravel에서 지원하는 데이터베이스 버전은 [데이터베이스 지원 문서](/docs/12.x/database#introduction)를 참고하시기 바랍니다.

<div class="overflow-auto">

| 버전   | PHP (*)   | 릴리즈              | 버그 수정 종료일        | 보안 수정 종료일       |
| ------ |----------| ------------------- | ---------------------- | ---------------------- |
| 10     | 8.1 - 8.3| 2023년 2월 14일     | 2024년 8월 6일         | 2025년 2월 4일         |
| 11     | 8.2 - 8.4| 2024년 3월 12일     | 2025년 9월 3일         | 2026년 3월 12일        |
| 12     | 8.2 - 8.5| 2025년 2월 24일     | 2026년 8월 13일        | 2027년 2월 24일        |
| 13     | 8.3 - 8.5| 2026년 1분기        | 2027년 3분기           | 2028년 1분기           |

</div>

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>지원 종료</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>보안 수정만 제공</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
## Laravel 12

Laravel 12는 기존 Laravel 11.x의 개선 사항을 바탕으로 업스트림 의존성 업데이트와 함께 React, Svelte, Vue, Livewire에 대한 새로운 스타터 키트(starter kits)를 도입하였습니다. 이 스타터 키트에는 사용자인증을 위한 [WorkOS AuthKit](https://authkit.com)을 옵션으로 제공합니다. WorkOS로 제공되는 스타터 키트는 소셜 인증, 패스키(passkey), SSO(싱글 사인온) 지원을 포함합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 호환성 깨짐 (Minimal Breaking Changes)

이번 릴리즈 주기에서는 호환성이 깨지는 변경을 최소화하는 데 중점을 두었습니다. 대신, 기존 애플리케이션에 영향을 주지 않으면서 연중 지속적으로 품질 개선을 제공하는 것에 전념했습니다.

따라서 Laravel 12 릴리즈는 기존 의존성 업그레이드를 위한 비교적 소규모의 "유지 보수 릴리즈"입니다. 이로 인해 대부분의 Laravel 애플리케이션은 애플리케이션 코드를 변경하지 않고도 Laravel 12로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 키트

Laravel 12는 React, Svelte, Vue, Livewire용 새로운 [애플리케이션 스타터 키트](/docs/12.x/starter-kits)를 제공합니다. React, Svelte, Vue 스타터 키트는 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하고, Livewire 스타터 키트는 Tailwind 기반 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

React, Svelte, Vue, Livewire 스타터 키트 모두 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 추가로, 각 스타터 키트에는 [WorkOS AuthKit 기반](https://authkit.com) 변형도 도입되어 소셜 인증, 패스키, SSO 지원이 제공됩니다. WorkOS는 월간 활성 사용자 1백만 명까지 무료 인증을 제공합니다.

새로운 애플리케이션 스타터 키트가 도입됨에 따라, Laravel Breeze와 Laravel Jetstream에는 더 이상 추가 업데이트가 제공되지 않습니다.

새로운 스타터 키트를 시작하려면 [스타터 키트 문서](/docs/12.x/starter-kits)를 참고하세요.
