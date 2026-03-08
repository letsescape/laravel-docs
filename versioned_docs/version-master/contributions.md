# 기여 가이드 (Contribution Guide)

- [버그 리포트](#bug-reports)
- [지원 질문](#support-questions)
- [코어 개발 논의](#core-development-discussion)
- [어떤 브랜치를 사용해야 하나요?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [행동 강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 리포트

활발한 협업을 장려하기 위해 Laravel은 단순한 버그 리포트보다는 **pull request** 제출을 강력히 권장합니다. Pull request는 **"ready for review" 상태**로 표시되어 있어야 하며(즉, "draft" 상태가 아니어야 합니다), 새 기능에 대한 모든 테스트가 통과한 경우에만 검토됩니다. 오랜 시간 활동이 없고 "draft" 상태로 남아 있는 pull request는 며칠 후 자동으로 닫힙니다.

하지만 버그 리포트를 작성하는 경우, **제목과 문제에 대한 명확한 설명**을 반드시 포함해야 합니다. 또한 가능한 한 많은 관련 정보와 함께 **문제를 재현할 수 있는 코드 예제**를 제공해야 합니다. 버그 리포트의 목적은 자신뿐만 아니라 다른 사람들도 쉽게 버그를 재현하고 수정할 수 있도록 만드는 것입니다.

버그 리포트는 동일한 문제를 겪는 다른 사람들이 함께 해결에 참여할 수 있기를 기대하며 작성됩니다. 버그 리포트를 작성했다고 해서 자동으로 누군가가 바로 대응하거나 수정해 줄 것이라고 기대해서는 안 됩니다. 버그 리포트의 목적은 문제 해결을 시작할 수 있는 기반을 만드는 것입니다. 직접 기여하고 싶다면 [이슈 트래커에 등록된 버그](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 수정하는 방식으로 도움을 줄 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub에 로그인되어 있어야 합니다.

Laravel을 사용하는 동안 DocBlock, PHPStan, 또는 IDE 경고가 잘못 표시되는 것을 발견했다면 GitHub 이슈를 생성하지 마십시오. 대신 해당 문제를 수정하는 **pull request**를 제출해 주십시오.

Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트마다 별도의 저장소(repository)가 존재합니다.

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

Laravel의 GitHub 이슈 트래커는 **Laravel 사용 방법에 대한 도움이나 지원을 제공하기 위한 공간이 아닙니다**. 대신 다음 채널 중 하나를 사용하십시오.

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
## 코어 개발 논의

Laravel 프레임워크 저장소의 [GitHub discussion board](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 Laravel 동작에 대한 개선 사항을 제안할 수 있습니다. 새로운 기능을 제안할 경우, 해당 기능을 완성하기 위해 필요한 코드의 일부라도 직접 구현할 의지가 있어야 합니다.

버그, 새로운 기능, 기존 기능의 구현 방식 등에 대한 비공식 논의는 [Laravel Discord 서버](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 유지 관리자(maintainer)인 Taylor Otwell은 보통 평일 오전 8시부터 오후 5시까지(UTC-06:00 또는 America/Chicago) 해당 채널에 접속해 있으며, 그 외 시간에도 간헐적으로 참여합니다.

<a name="which-branch"></a>
## 어떤 브랜치를 사용해야 하나요?

**모든** 버그 수정은 버그 수정을 지원하는 **최신 버전 브랜치**(현재 `12.x`)로 보내야 합니다. 버그 수정은 **다음 릴리스에만 존재하는 기능을 수정하는 경우가 아니라면 절대 `master` 브랜치로 보내면 안 됩니다.**

현재 릴리스와 **완전히 하위 호환(fully backward compatible)** 되는 **소규모 기능(Minor feature)** 은 최신 안정 브랜치(현재 `12.x`)로 보낼 수 있습니다.

**대규모 신규 기능(Major feature)** 이나 **호환성이 깨지는 변경(Breaking change)** 이 포함된 기능은 항상 **다음 릴리스가 포함된 `master` 브랜치**로 보내야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 자산

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 대부분의 파일처럼 **컴파일된 파일에 영향을 주는 변경 사항**을 제출하는 경우, **컴파일된 파일은 커밋하지 마십시오.**

이 파일들은 크기가 매우 커서 유지 관리자가 현실적으로 검토하기 어렵습니다. 또한 이러한 파일은 **Laravel에 악성 코드를 삽입하는 공격 경로로 악용될 수 있습니다.** 이를 방지하기 위해 모든 컴파일된 파일은 Laravel 유지 관리자가 직접 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견했다면 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 Taylor Otwell에게 이메일을 보내 주십시오. 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

다음은 올바른 Laravel 문서 블록의 예시입니다. `@param` 속성 뒤에는 **두 개의 공백**, 인수 타입, 다시 **두 개의 공백**, 그리고 마지막으로 변수 이름이 오는 형식을 사용합니다.

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

`@param` 또는 `@return` 속성이 **네이티브 타입 선언으로 충분히 표현되는 경우**에는 해당 속성을 제거할 수 있습니다.

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

그러나 네이티브 타입이 **제네릭 타입(generic type)** 인 경우에는 `@param` 또는 `@return` 속성을 사용하여 제네릭 타입을 명시해야 합니다.

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

코드 스타일이 완벽하지 않아도 걱정하지 마십시오. [StyleCI](https://styleci.io/)가 pull request가 병합된 후 Laravel 저장소에 **스타일 수정 사항을 자동으로 병합**합니다. 이를 통해 우리는 코드 스타일이 아니라 **기여 내용 자체에 집중**할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령은 Ruby 행동 강령에서 파생되었습니다. 행동 강령 위반은 Taylor Otwell (taylor@laravel.com)에게 보고할 수 있습니다.

<div class="content-list" markdown="1">

- 참가자는 서로 다른 의견에 대해 관용적인 태도를 가져야 합니다.
- 참가자는 언어와 행동에서 개인 공격이나 비방성 발언이 없도록 해야 합니다.
- 다른 사람의 말과 행동을 해석할 때는 항상 **선의(good intentions)** 를 가정해야 합니다.
- 합리적으로 괴롭힘으로 간주될 수 있는 행동은 용납되지 않습니다.

</div>