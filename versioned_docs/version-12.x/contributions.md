# 기여 가이드 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 토론](#core-development-discussion)
- [어떤 브랜치로 보내야 하나요?](#which-branch)
- [컴파일된 에셋](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

활발한 협업을 장려하기 위해 Laravel은 단순한 버그 리포트보다 **pull request 제출을 강력히 권장**합니다. Pull request는 "draft" 상태가 아니라 **"ready for review" 상태로 표시되고**, 새 기능과 관련된 **모든 테스트가 통과했을 때만 검토**됩니다. "draft" 상태로 오래 방치된 비활성 Pull request는 며칠 후 자동으로 닫힙니다.

하지만 버그 리포트를 작성하는 경우, 이슈에는 **제목과 문제에 대한 명확한 설명**이 반드시 포함되어야 합니다. 또한 가능한 한 **관련 정보와 문제를 재현할 수 있는 코드 예제**를 함께 제공해야 합니다. 버그 리포트의 목표는 **자신과 다른 사람들이 버그를 쉽게 재현하고 수정할 수 있도록 돕는 것**입니다.

버그 리포트는 동일한 문제를 겪는 다른 사람들과 함께 해결하기 위해 작성된다는 점을 기억하십시오. 버그 리포트가 자동으로 활발히 처리되거나 다른 사람이 바로 수정해 줄 것이라고 기대해서는 안 됩니다. 버그 리포트를 작성하는 것은 문제 해결을 시작하기 위한 출발점입니다. 직접 기여하고 싶다면 [issue tracker에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 수정하는 데 도움을 줄 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub에 로그인되어 있어야 합니다.

Laravel을 사용하는 동안 **부적절한 DocBlock, PHPStan, 또는 IDE 경고**를 발견했다면 GitHub 이슈를 생성하지 마십시오. 대신 해당 문제를 수정하는 **pull request를 제출**해 주십시오.

Laravel의 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트마다 별도의 저장소가 존재합니다.

<div class="content-list" markdown="1">

- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Boost](https://github.com/laravel/boost)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel Reverb](https://github.com/laravel/reverb)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Livewire Starter Kit](https://github.com/laravel/livewire-starter-kit)
- [Laravel React Starter Kit](https://github.com/laravel/react-starter-kit)
- [Laravel Svelte Starter Kit](https://github.com/laravel/svelte-starter-kit)
- [Laravel Vue Starter Kit](https://github.com/laravel/vue-starter-kit)

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 이슈 트래커는 **Laravel 사용 방법에 대한 도움이나 지원을 제공하기 위한 용도**가 아닙니다. 대신 다음 채널 중 하나를 이용하십시오.

<div class="content-list" markdown="1">

- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="core-development-discussion"></a>
## 코어 개발 토론

새로운 기능 제안이나 기존 Laravel 동작에 대한 개선 제안은 Laravel framework 저장소의 [GitHub discussion board](https://github.com/laravel/framework/discussions)에서 할 수 있습니다. 새로운 기능을 제안하는 경우, 해당 기능을 완성하는 데 필요한 코드의 일부라도 **직접 구현할 의지**가 있어야 합니다.

버그, 새로운 기능, 기존 기능의 구현 방식에 대한 비공식 토론은 [Laravel Discord server](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 유지 관리자인 Taylor Otwell은 일반적으로 평일 오전 8시부터 오후 5시까지(UTC-06:00 또는 America/Chicago) 해당 채널에 접속해 있으며, 그 외 시간에도 간헐적으로 참여합니다.

<a name="which-branch"></a>
## 어떤 브랜치로 보내야 하나요?

**모든** 버그 수정은 **버그 수정이 지원되는 최신 버전 브랜치**로 보내야 합니다(현재 `12.x`). 버그 수정은 **다음 릴리스에서만 존재하는 기능을 수정하는 경우가 아니라면 절대 `master` 브랜치로 보내면 안 됩니다.**

현재 릴리스와 **완전히 하위 호환(backward compatible)** 되는 **작은 기능 추가**는 **최신 안정 브랜치**로 보낼 수 있습니다(현재 `12.x`).

**대규모 새 기능** 또는 **호환성을 깨는 변경 사항(breaking changes)** 이 포함된 기능은 항상 **다음 릴리스를 포함하는 `master` 브랜치**로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 에셋

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 대부분의 파일처럼 **컴파일된 파일에 영향을 주는 변경 사항**을 제출하는 경우, **컴파일된 파일은 커밋하지 마십시오.**  

컴파일된 파일은 용량이 크기 때문에 유지 관리자가 현실적으로 검토하기 어렵습니다. 또한 이는 Laravel에 **악성 코드를 삽입하는 공격 경로**로 악용될 수 있습니다. 이러한 문제를 방지하기 위해 **모든 컴파일된 파일은 Laravel 유지 관리자가 직접 생성하고 커밋합니다.**

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견한 경우, Taylor Otwell에게 이메일로 알려주십시오: <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>.  
모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

다음은 올바른 Laravel 문서 블록의 예시입니다. `@param` 속성 뒤에는 **두 칸의 공백**, **인수 타입**, **다시 두 칸의 공백**, 그리고 **변수 이름**이 순서대로 위치합니다.

```php
/**
 * Register a binding with the container.
 *
 * @param  string|array  $abstract
 * @param  \Closure|string|null  $concrete
 * @param  bool  $shared
 * @return void
 *
 * @throws \Exception
 */
public function bind($abstract, $concrete = null, $shared = false)
{
    // ...
}
```

`@param` 또는 `@return` 속성이 **native 타입 선언으로 인해 중복되는 경우**에는 제거할 수 있습니다.

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

하지만 native 타입이 **제네릭 타입인 경우**에는 `@param` 또는 `@return` 속성을 사용하여 제네릭 타입을 명시해야 합니다.

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```

<a name="styleci"></a>
### StyleCI

코드 스타일이 완벽하지 않아도 걱정하지 마십시오! [StyleCI](https://styleci.io/)가 Pull request가 병합된 후 자동으로 코드 스타일 수정 사항을 Laravel 저장소에 반영합니다. 덕분에 우리는 코드 스타일보다 **기여 내용 자체에 집중**할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령은 Ruby의 행동 강령을 기반으로 합니다. 행동 강령 위반 사항은 Taylor Otwell(taylor@laravel.com)에게 보고할 수 있습니다.

<div class="content-list" markdown="1">

- 참여자는 서로 다른 의견에 대해 관용적인 태도를 가져야 합니다.
- 참여자는 개인 공격이나 비하 발언이 없는 언어와 행동을 사용해야 합니다.
- 다른 사람의 말과 행동을 해석할 때는 항상 선의를 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>