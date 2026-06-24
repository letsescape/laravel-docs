<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel과 주요 1차 제공 패키지들은 [Semantic Versioning](https://semver.org)을 따릅니다. 주요 프레임워크 릴리스는 매년(대략 1분기)에 출시되며, 마이너 및 패치 릴리스는 매주 출시될 수 있습니다. 마이너 및 패치 릴리스에는 절대로 **호환성이 깨지는 변경사항**이 포함되어서는 안 됩니다.

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^12.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
애플리케이션이나 패키지에서 Laravel 프레임워크 및 컴포넌트를 참조할 때는 반드시 `^12.0`과 같은 버전 제약 조건을 사용하시기 바랍니다. Laravel의 주요 릴리스에는 호환성이 깨지는 변경 사항이 포함될 수 있기 때문입니다. 그러나, 새로운 주요 릴리스로 하루 이내에 업그레이드할 수 있도록 항상 최선을 다하고 있습니다.

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성 정책에 포함되지 않습니다. 필요에 따라 Laravel 코드베이스 개선을 위해 함수 인수명을 변경할 수 있습니다. 따라서, Laravel 메서드를 호출할 때 네임드 인수를 사용할 경우 인수명이 향후 변경될 수 있음을 유념하시고 신중하게 사용해야 합니다.

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/12.x/database#introduction). -->
모든 Laravel 릴리스는 버그 수정이 18개월, 보안 수정이 2년 동안 제공됩니다. 추가 라이브러리의 경우, 오직 최신 주요 릴리스만 버그 수정을 받습니다. 또한, Laravel에서 지원하는 데이터베이스 버전은 [supported by Laravel](/docs/12.x/database#introduction)를 참고하시기 바랍니다.

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| 버전   | PHP (*)   | 릴리스              | 버그 수정 종료일        | 보안 수정 종료일       |
| ------ |----------| ------------------- | ---------------------- | ---------------------- |
| 10     | 8.1 - 8.3| 2023년 2월 14일     | 2024년 8월 6일         | 2025년 2월 4일         |
| 11     | 8.2 - 8.4| 2024년 3월 12일     | 2025년 9월 3일         | 2026년 3월 12일        |
| 12     | 8.2 - 8.5| 2025년 2월 24일     | 2026년 8월 13일        | 2027년 2월 24일        |
| 13     | 8.3 - 8.5| 2026년 1분기        | 2027년 3분기           | 2028년 1분기           |

<!-- </div> -->
</div>

<!--
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>
-->
<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>지원 종료</div>
</div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>보안 수정만 제공</div>
    </div>
</div>

<!-- (*) Supported PHP versions -->
(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
<!-- ## Laravel 12 -->
## Laravel 12

<!-- Laravel 12 continues the improvements made in Laravel 11.x by updating upstream dependencies and introducing new starter kits for React, Svelte, Vue, and Livewire, including the option of using [WorkOS AuthKit](https://authkit.com) for user authentication. The WorkOS variant of our starter kits offers social authentication, passkeys, and SSO support. -->
Laravel 12는 기존 Laravel 11.x의 개선 사항을 바탕으로 업스트림 의존성 업데이트와 함께 React, Svelte, Vue, Livewire에 대한 새로운 스타터 키트(starter kits)를 도입하였습니다. 이 스타터 키트에는 사용자인증을 위한 [WorkOS AuthKit](https://authkit.com)을 옵션으로 제공합니다. WorkOS로 제공되는 스타터 키트는 소셜 인증, 패스키(passkey), SSO(싱글 사인온) 지원을 포함합니다.

<a name="minimal-breaking-changes"></a>
<!-- ### Minimal Breaking Changes -->
### Minimal Breaking Changes

<!-- Much of our focus during this release cycle has been minimizing breaking changes. Instead, we have dedicated ourselves to shipping continuous quality-of-life improvements throughout the year that do not break existing applications. -->
이번 릴리스 주기에서는 호환성이 깨지는 변경을 최소화하는 데 중점을 두었습니다. 대신, 기존 애플리케이션에 영향을 주지 않으면서 연중 지속적으로 품질 개선을 제공하는 것에 전념했습니다.

<!-- Therefore, the Laravel 12 release is a relatively minor "maintenance release" in order to upgrade existing dependencies. In light of this, most Laravel applications may upgrade to Laravel 12 without changing any application code. -->
따라서 Laravel 12 릴리스는 기존 의존성 업그레이드를 위한 비교적 소규모의 "유지 보수 릴리스"입니다. 이로 인해 대부분의 Laravel 애플리케이션은 애플리케이션 코드를 변경하지 않고도 Laravel 12로 업그레이드할 수 있습니다.

<a name="new-application-starter-kits"></a>
<!-- ### New Application Starter Kits -->
### New Application Starter Kits

<!-- Laravel 12 introduces new [application starter kits](/docs/12.x/starter-kits) for React, Svelte, Vue, and Livewire. The React, Svelte, and Vue starter kits utilize Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), and Tailwind, while the Livewire starter kits utilize the Tailwind-based [Flux UI](https://fluxui.dev) component library and Laravel Volt. -->
Laravel 12는 React, Svelte, Vue, Livewire용 새로운 [application starter kits](/docs/12.x/starter-kits)를 제공합니다. React, Svelte, Vue 스타터 키트는 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 활용하고, Livewire 스타터 키트는 Tailwind 기반 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

<!-- The React, Svelte, Vue, and Livewire starter kits all utilize Laravel's built-in authentication system to offer login, registration, password reset, email verification, and more. In addition, we are introducing a [WorkOS AuthKit-powered](https://authkit.com) variant of each starter kit, offering social authentication, passkeys, and SSO support. WorkOS offers free authentication for applications up to 1 million monthly active users. -->
React, Svelte, Vue, Livewire 스타터 키트 모두 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등 다양한 기능을 제공합니다. 추가로, 각 스타터 키트에는 [WorkOS AuthKit-powered](https://authkit.com) 변형도 도입되어 소셜 인증, 패스키, SSO 지원이 제공됩니다. WorkOS는 월간 활성 사용자 1백만 명까지 무료 인증을 제공합니다.

<!-- With the introduction of our new application starter kits, Laravel Breeze and Laravel Jetstream will no longer receive additional updates. -->
새로운 애플리케이션 스타터 키트가 도입됨에 따라, Laravel Breeze와 Laravel Jetstream에는 더 이상 추가 업데이트가 제공되지 않습니다.

<!-- To get started with our new starter kits, check out the [starter kit documentation](/docs/12.x/starter-kits). -->
새로운 스타터 키트를 시작하려면 [starter kit documentation](/docs/12.x/starter-kits)를 참고하세요.
