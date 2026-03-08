# 릴리스 노트 (Release Notes)

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
## 버전 관리 체계 (Versioning Scheme)

Laravel과 그 외 공식(퍼스트 파티) 패키지들은 [시맨틱 버저닝(Semantic Versioning)](https://semver.org)을 따릅니다. 프레임워크의 메이저 릴리스는 매년(대략 Q1)에 한 번 출시되며, 마이너 및 패치 릴리스는 필요에 따라 거의 매주 출시될 수 있습니다. 마이너 및 패치 릴리스에는 **절대로 호환성이 깨지는 변경(Breaking Changes)** 이 포함되지 않습니다.

애플리케이션이나 패키지에서 Laravel 프레임워크 또는 그 구성 요소를 참조할 때는 항상 `^12.0`과 같은 버전 제약 조건을 사용해야 합니다. Laravel의 메이저 릴리스에는 호환성이 깨지는 변경이 포함되기 때문입니다. 다만 Laravel 팀은 새로운 메이저 릴리스로 **하루 이내에 업그레이드할 수 있도록** 유지하는 것을 목표로 하고 있습니다.

<a name="named-arguments"></a>
#### Named Arguments

[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 하위 호환성(backwards compatibility) 가이드라인에 포함되지 않습니다. Laravel 코드베이스를 개선하기 위해 필요할 경우 함수 인수 이름을 변경할 수 있습니다. 따라서 Laravel 메서드를 호출할 때 named arguments를 사용하는 경우, 향후 파라미터 이름이 변경될 수 있다는 점을 이해하고 **신중하게 사용해야 합니다.**

<a name="support-policy"></a>
## 지원 정책 (Support Policy)

모든 Laravel 릴리스는 **18개월 동안 버그 수정**이 제공되며, **2년 동안 보안 수정**이 제공됩니다. 추가 라이브러리의 경우 **가장 최신 메이저 릴리스만 버그 수정 지원**을 받습니다. 또한 Laravel에서 지원하는 데이터베이스 버전에 대해서는 [supported by Laravel](/docs/master/database#introduction) 문서를 참고하시기 바랍니다.

<div class="overflow-auto">

| Version | PHP (*)   | Release             | Bug Fixes Until     | Security Fixes Until |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1 - 8.3 | February 14th, 2023 | August 6th, 2024    | February 4th, 2025   |
| 11      | 8.2 - 8.4 | March 12th, 2024    | September 3rd, 2025 | March 12th, 2026     |
| 12      | 8.2 - 8.5 | February 24th, 2025 | August 13th, 2026   | February 24th, 2027  |
| 13      | 8.3 - 8.5 | Q1 2026             | Q3 2027             | Q1 2028              |

</div>

<div class="version-colors">
```
<div class="end-of-life">
    <div class="color-box"></div>
    <div>End of life</div>
</div>
<div class="security-fixes">
    <div class="color-box"></div>
    <div>Security fixes only</div>
</div>
```
</div>

(*) 지원되는 PHP 버전

<a name="laravel-12"></a>
## Laravel 12

Laravel 12는 Laravel 11.x에서 이루어진 개선을 이어가며, 상위 의존성(upstream dependencies)을 업데이트하고 React, Svelte, Vue, Livewire를 위한 새로운 스타터 키트를 도입했습니다. 또한 사용자 인증을 위해 [WorkOS AuthKit](https://authkit.com)을 사용할 수 있는 옵션도 제공합니다. WorkOS 기반 스타터 키트는 소셜 인증, 패스키(passkeys), SSO를 지원합니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 호환성 변경

이번 릴리스 주기 동안 Laravel 팀은 **호환성을 깨뜨리는 변경을 최소화하는 것**에 많은 노력을 기울였습니다. 대신 기존 애플리케이션을 깨뜨리지 않으면서 개발 경험을 개선하는 다양한 품질 향상(Quality of Life) 개선을 연중 지속적으로 제공하는 데 집중했습니다.

따라서 Laravel 12 릴리스는 기존 의존성을 업그레이드하기 위한 비교적 작은 **“유지보수 릴리스(maintenance release)”** 에 가깝습니다. 이로 인해 대부분의 Laravel 애플리케이션은 **애플리케이션 코드를 변경하지 않고도 Laravel 12로 업그레이드할 수 있습니다.**

<a name="new-application-starter-kits"></a>
### 새로운 애플리케이션 스타터 키트

Laravel 12는 React, Svelte, Vue, Livewire를 위한 새로운 [application starter kits](/docs/master/starter-kits)를 제공합니다. React, Svelte, Vue 스타터 키트는 Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), Tailwind를 사용하며, Livewire 스타터 키트는 Tailwind 기반의 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리와 Laravel Volt를 사용합니다.

React, Svelte, Vue, Livewire 스타터 키트는 모두 Laravel의 내장 인증 시스템을 사용하여 로그인, 회원가입, 비밀번호 재설정, 이메일 인증 등의 기능을 제공합니다. 또한 각 스타터 키트에 대해 [WorkOS AuthKit-powered](https://authkit.com) 변형도 제공되며, 이를 통해 소셜 인증, 패스키, SSO 지원을 사용할 수 있습니다. WorkOS는 **월간 활성 사용자 100만 명까지 무료 인증 서비스**를 제공합니다.

새로운 애플리케이션 스타터 키트가 도입됨에 따라 **Laravel Breeze와 Laravel Jetstream은 더 이상 추가 업데이트를 받지 않습니다.**

새로운 스타터 키트를 시작하려면 [starter kit documentation](/docs/master/starter-kits)을 참고하시기 바랍니다.