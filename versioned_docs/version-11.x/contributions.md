<!-- # Contribution Guide -->
# Contribution Guide

- [Bug Reports](#bug-reports)
- [Support Questions](#support-questions)
- [Core Development Discussion](#core-development-discussion)
- [Which Branch?](#which-branch)
- [Compiled Assets](#compiled-assets)
- [Security Vulnerabilities](#security-vulnerabilities)
- [Coding Style](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [Code of Conduct](#code-of-conduct)

<a name="bug-reports"></a>
<!-- ## Bug Reports -->
## Bug Reports

<!-- To encourage active collaboration, Laravel strongly encourages pull requests, not just bug reports. Pull requests will only be reviewed when marked as "ready for review" (not in the "draft" state) and all tests for new features are passing. Lingering, non-active pull requests left in the "draft" state will be closed after a few days. -->
Laravel은 적극적인 협업을 장려하기 위해 단순한 버그 리포트뿐 아니라 직접적인 pull request 제출을 강력히 권장합니다. pull request는 반드시 "ready for review"(검토 가능) 상태로 표시되고(즉, "draft" 상태가 아니어야 함), 새로운 기능에 대한 모든 테스트가 통과해야만 검토됩니다. 장기간 "draft" 상태로 남아있고 활동이 없는 pull request는 며칠 후 자동으로 닫힙니다.

<!-- However, if you file a bug report, your issue should contain a title and a clear description of the issue. You should also include as much relevant information as possible and a code sample that demonstrates the issue. The goal of a bug report is to make it easy for yourself - and others - to replicate the bug and develop a fix. -->
버그 리포트를 남길 경우, 이슈에는 제목과 문제에 대한 명확한 설명이 포함되어야 하며, 가능하다면 관련 정보를 최대한 많이 제공하고, 문제를 재현할 수 있는 코드 샘플을 첨부해야 합니다. 버그 리포트의 목적은 여러분 자신과 다른 사람들이 해당 버그를 손쉽게 재현하고 수정할 수 있도록 돕는 데 있습니다.

<!-- Remember, bug reports are created in the hope that others with the same problem will be able to collaborate with you on solving it. Do not expect that the bug report will automatically see any activity or that others will jump to fix it. Creating a bug report serves to help yourself and others start on the path of fixing the problem. If you want to chip in, you can help out by fixing [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). You must be authenticated with GitHub to view all of Laravel's issues. -->
버그 리포트는 같은 문제를 겪고 있는 다른 사람들이 문제 해결에 함께 참여할 수 있도록 작성되는 것임을 기억해 주세요. 버그 리포트를 올렸다고 해서 반드시 바로 개선이 이루어지거나, 다른 사람이 문제를 곧바로 고쳐줄 것으로 기대해서는 안 됩니다. 버그 리포트는 문제를 해결하는 출발점 역할을 한다고 생각하면 됩니다. 만약 직접 기여하고 싶다면, [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중 일부를 직접 수정해볼 수도 있습니다. 참고로 Laravel의 모든 이슈를 보려면 GitHub에 로그인되어 있어야 합니다.

<!-- If you notice improper DocBlock, PHPStan, or IDE warnings while using Laravel, do not create a GitHub issue. Instead, please submit a pull request to fix the problem. -->
만약 Laravel을 사용하다가 올바르지 않은 DocBlock, PHPStan, IDE 경고 등을 발견했다면, GitHub 이슈를 생성하지 마시고 pull request로 직접 문제를 수정해 주시기 바랍니다.

<!-- The Laravel source code is managed on GitHub, and there are repositories for each of the Laravel projects: -->
Laravel의 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트별로 별개의 저장소가 존재합니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Breeze](https://github.com/laravel/breeze)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead) ([Build Scripts](https://github.com/laravel/settler))
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
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
- [Laravel Website](https://github.com/laravel/laravel.com)
-->
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Breeze](https://github.com/laravel/breeze)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead) ([Build Scripts](https://github.com/laravel/settler))
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
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
- [Laravel Website](https://github.com/laravel/laravel.com)

<!-- </div> -->
</div>

<a name="support-questions"></a>
<!-- ## Support Questions -->
## Support Questions

<!-- Laravel's GitHub issue trackers are not intended to provide Laravel help or support. Instead, use one of the following channels: -->
Laravel의 GitHub 이슈 트래커는 Laravel 사용법이나 기술 지원을 제공하기 위한 공간이 아닙니다. 대신 다음 채널 중 하나를 이용해 주세요.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)
-->
- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

<!-- </div> -->
</div>

<a name="core-development-discussion"></a>
<!-- ## Core Development Discussion -->
## Core Development Discussion

<!-- You may propose new features or improvements of existing Laravel behavior in the Laravel framework repository's [GitHub discussion board](https://github.com/laravel/framework/discussions). If you propose a new feature, please be willing to implement at least some of the code that would be needed to complete the feature. -->
Laravel 프레임워크의 [GitHub discussion board](https://github.com/laravel/framework/discussions)에서 새로운 기능 제안이나 기존 동작 개선에 대한 의견을 남길 수 있습니다. 새로운 기능을 제안할 경우, 해당 기능을 완성하는 데 필요한 코드 중 일부라도 스스로 구현할 의지가 있는지 확인해 주세요.

<!-- Informal discussion regarding bugs, new features, and implementation of existing features takes place in the `#internals` channel of the [Laravel Discord server](https://discord.gg/laravel). Taylor Otwell, the maintainer of Laravel, is typically present in the channel on weekdays from 8am-5pm (UTC-06:00 or America/Chicago), and sporadically present in the channel at other times. -->
버그, 새로운 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord server](https://discord.gg/laravel) 내 `#internals` 채널에서 이루어집니다. Laravel의 관리자인 Taylor Otwell은 평일(UTC-06:00 또는 America/Chicago 기준) 오전 8시부터 오후 5시까지는 주로 이 채널에 상주하며, 그 외 시간에도 간헐적으로 참여합니다.

<a name="which-branch"></a>
<!-- ## Which Branch? -->
## Which Branch?

<!-- **All** bug fixes should be sent to the latest version that supports bug fixes (currently `11.x`). Bug fixes should **never** be sent to the `master` branch unless they fix features that exist only in the upcoming release. -->
**모든** 버그 수정은 버그 수정이 지원되는 최신 버전(현재는 `11.x`)에 보내져야 합니다. 이미 공개된 버그 수정에 대해서는 **절대로** `master` 브랜치로 pull request를 보내면 안 되며, 오직 차기 릴리스에만 해당되는 새로운 버그 수정인 경우에만 예외가 적용됩니다.

<!-- **Minor** features that are **fully backward compatible** with the current release may be sent to the latest stable branch (currently `11.x`). -->
**완전히 하위 호환이 보장되는** **경미한** 기능 추가의 경우에도 최신 안정 브랜치(현재는 `11.x`)로 보내야 합니다.

<!-- **Major** new features or features with breaking changes should always be sent to the `master` branch, which contains the upcoming release. -->
**주요** 신규 기능이나 기존 기능에 변경(하위 호환성 파괴)이 있는 경우에는 항상 차기 릴리스가 준비되는 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
<!-- ## Compiled Assets -->
## Compiled Assets

<!-- If you are submitting a change that will affect a compiled file, such as most of the files in `resources/css` or `resources/js` of the `laravel/laravel` repository, do not commit the compiled files. Due to their large size, they cannot realistically be reviewed by a maintainer. This could be exploited as a way to inject malicious code into Laravel. In order to defensively prevent this, all compiled files will be generated and committed by Laravel maintainers. -->
`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js`와 같이 컴파일된 파일에 영향을 주는 변경 사항을 제출하는 경우, 컴파일된 파일 자체는 커밋하지 마세요. 이러한 파일들은 용량이 크고, 실제로 관리자가 검토하기 어려우므로, 악의적인 코드가 삽입될 위험이 있습니다. 이런 문제를 방지하기 위해 모든 컴파일된 파일은 Laravel 담당자만 생성하고 커밋합니다.

<a name="security-vulnerabilities"></a>
<!-- ## Security Vulnerabilities -->
## Security Vulnerabilities

<!-- If you discover a security vulnerability within Laravel, please send an email to Taylor Otwell at <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. All security vulnerabilities will be promptly addressed. -->
Laravel에서 보안 취약점을 발견한 경우, Taylor Otwell에게 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a> 으로 이메일을 보내주세요. 모든 보안 취약점은 신속하게 대응됩니다.

<a name="coding-style"></a>
<!-- ## Coding Style -->
## Coding Style

<!-- Laravel follows the [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) coding standard and the [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) autoloading standard. -->
Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 스타일 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
<!-- ### PHPDoc -->
### PHPDoc

<!-- Below is an example of a valid Laravel documentation block. Note that the `@param` attribute is followed by two spaces, the argument type, two more spaces, and finally the variable name: -->
아래는 Laravel 문서화 주석 블록(PHPDoc)의 올바른 예시입니다. `@param` 속성 다음에는 공백 두 칸, 인수 타입, 다시 공백 두 칸, 그리고 변수명이 순서대로 들어가야 함에 주의하세요.

```
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

<!-- When the `@param` or `@return` attributes are redundant due to the use of native types, they can be removed: -->
만약 네이티브 타입 지정을 통해 `@param`이나 `@return` 속성이 불필요할 경우, 해당 속성은 생략할 수 있습니다.

```
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    //
}
```

<!-- However, when the native type is generic, please specify the generic type through the use of the `@param` or `@return` attributes: -->
하지만 네이티브 타입이 제네릭인 경우, `@param` 또는 `@return` 주석을 사용해 제네릭 타입을 명시해 주세요.

```
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
<!-- ### StyleCI -->
### StyleCI

<!-- Don't worry if your code styling isn't perfect! [StyleCI](https://styleci.io/) will automatically merge any style fixes into the Laravel repository after pull requests are merged. This allows us to focus on the content of the contribution and not the code style. -->
코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 pull request가 병합된 후 Laravel 저장소에 자동으로 스타일 관련 수정을 반영합니다. 이는 기여 내용의 실질적인 내용에 집중할 수 있도록 도와줍니다.

<a name="code-of-conduct"></a>
<!-- ## Code of Conduct -->
## Code of Conduct

<!-- The Laravel code of conduct is derived from the Ruby code of conduct. Any violations of the code of conduct may be reported to Taylor Otwell (taylor@laravel.com): -->
Laravel의 행동 강령은 Ruby의 행동 강령을 바탕으로 만들어졌습니다. 행동 강령 위반 사항은 Taylor Otwell(taylor@laravel.com)에게 신고하실 수 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should always assume good intentions.
- Behavior that can be reasonably considered harassment will not be tolerated.
-->
- 참가자는 서로 다른 의견에 대해 관용적으로 대해야 합니다.
- 참가자는 자신의 언행에서 인신공격이나 비방성 표현이 없도록 주의해야 합니다.
- 타인의 말이나 행동을 해석할 때, 항상 긍정적 의도를 전제로 삼아야 합니다.
- 합리적으로 괴롭힘으로 여겨질 수 있는 행동은 용납되지 않습니다.

<!-- </div> -->
</div>