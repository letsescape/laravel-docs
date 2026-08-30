<!-- # Contribution Guide -->
# Contribution Guide

- [Bug Reports](#bug-reports)
- [Support Questions](#support-questions)
- [Core Development Discussion](#core-development-discussion)
- [Which Branch?](#which-branch)
- [Compiled Assets](#compiled-assets)
- [AI-Generated Contributions](#ai-generated-contributions)
- [Security Vulnerabilities](#security-vulnerabilities)
- [Coding Style](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [Code of Conduct](#code-of-conduct)

<a name="bug-reports"></a>
<!-- ## Bug Reports -->
## Bug Reports

<!-- To encourage active collaboration, Laravel strongly encourages pull requests, not just bug reports. Pull requests will only be reviewed when marked as "ready for review" (not in the "draft" state) and all tests for new features are passing. Lingering, non-active pull requests left in the "draft" state will be closed after a few days. -->
적극적인 협업을 장려하기 위해 Laravel은 단순한 버그 보고보다 pull request를 강력히 권장합니다. Pull request는 "ready for review"로 표시되어 있고("draft" 상태가 아니며), 새 기능에 대한 모든 테스트가 통과한 경우에만 검토됩니다. "draft" 상태로 남아 있는 오래된 비활성 pull request는 며칠 후 닫힙니다.

<!-- However, if you file a bug report, your issue should contain a title and a clear description of the issue. You should also include as much relevant information as possible and a code sample that demonstrates the issue. The goal of a bug report is to make it easy for yourself - and others - to replicate the bug and develop a fix. -->
하지만 버그 보고를 작성한다면, 이슈에는 제목과 문제에 대한 명확한 설명이 포함되어야 합니다. 또한 가능한 한 관련 정보를 많이 포함하고, 문제를 보여 주는 코드 예제도 함께 제공해야 합니다. 버그 보고의 목표는 자신과 다른 사람들이 버그를 쉽게 재현하고 수정 방법을 개발할 수 있도록 하는 것입니다.

<!-- Remember, bug reports are created in the hope that others with the same problem will be able to collaborate with you on solving it. Do not expect that the bug report will automatically see any activity or that others will jump to fix it. Creating a bug report serves to help yourself and others start on the path of fixing the problem. If you want to chip in, you can help out by fixing [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). You must be authenticated with GitHub to view all of Laravel's issues. -->
버그 보고는 같은 문제를 겪는 다른 사람들이 문제 해결에 함께 협력할 수 있기를 기대하며 작성된다는 점을 기억하세요. 버그 보고를 작성했다고 해서 자동으로 활동이 일어나거나, 다른 사람들이 바로 수정에 뛰어들 것이라고 기대해서는 안 됩니다. 버그 보고를 작성하는 것은 자신과 다른 사람들이 문제를 해결하기 위한 출발점을 마련하는 데 도움이 됩니다. 직접 기여하고 싶다면 [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel)를 수정하는 데 도움을 줄 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub에 인증되어 있어야 합니다.

<!-- If you notice improper DocBlock, PHPStan, or IDE warnings while using Laravel, do not create a GitHub issue. Instead, please submit a pull request to fix the problem. -->
Laravel을 사용하는 중에 부적절한 DocBlock, PHPStan 또는 IDE 경고를 발견했다면 GitHub 이슈를 만들지 마세요. 대신 문제를 수정하는 pull request를 제출해 주세요.

<!-- The Laravel source code is managed on GitHub, and there are repositories for each of the Laravel projects: -->
Laravel 소스 코드는 GitHub에서 관리되며, 각 Laravel 프로젝트마다 저장소가 있습니다.

<div class="content-list" markdown="1">

<!-- - [Laravel AI SDK](https://github.com/laravel/ai) - [Laravel Application](https://github.com/laravel/laravel) - [Laravel Art](https://github.com/laravel/art) - [Laravel Boost](https://github.com/laravel/boost) - [Laravel Documentation](https://github.com/laravel/docs) - [Laravel Dusk](https://github.com/laravel/dusk) - [Laravel Cashier Stripe](https://github.com/laravel/cashier) - [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) - [Laravel Echo](https://github.com/laravel/echo) - [Laravel Envoy](https://github.com/laravel/envoy) - [Laravel Folio](https://github.com/laravel/folio) - [Laravel Framework](https://github.com/laravel/framework) - [Laravel Horizon](https://github.com/laravel/horizon) - [Laravel Passport](https://github.com/laravel/passport) - [Laravel Pennant](https://github.com/laravel/pennant) - [Laravel Pint](https://github.com/laravel/pint) - [Laravel Prompts](https://github.com/laravel/prompts) - [Laravel Reverb](https://github.com/laravel/reverb) - [Laravel Sail](https://github.com/laravel/sail) - [Laravel Sanctum](https://github.com/laravel/sanctum) - [Laravel Scout](https://github.com/laravel/scout) - [Laravel Socialite](https://github.com/laravel/socialite) - [Laravel Telescope](https://github.com/laravel/telescope) - [Laravel Livewire Starter Kit](https://github.com/laravel/livewire-starter-kit) - [Laravel React Starter Kit](https://github.com/laravel/react-starter-kit) - [Laravel Svelte Starter Kit](https://github.com/laravel/svelte-starter-kit) - [Laravel Vue Starter Kit](https://github.com/laravel/vue-starter-kit) -->
- [Laravel AI SDK](https://github.com/laravel/ai)
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
<!-- ## Support Questions -->
## Support Questions

<!-- Laravel's GitHub issue trackers are not intended to provide Laravel help or support. Instead, use one of the following channels: -->
Laravel의 GitHub 이슈 트래커는 Laravel 도움말이나 지원을 제공하기 위한 곳이 아닙니다. 대신 다음 채널 중 하나를 이용하세요.

<div class="content-list" markdown="1">

<!-- - [GitHub Discussions](https://github.com/laravel/framework/discussions) - [Laracasts Forums](https://laracasts.com/discuss) - [Laravel.io Forums](https://laravel.io/forum) - [StackOverflow](https://stackoverflow.com/questions/tagged/laravel) - [Discord](https://discord.gg/laravel) - [Larachat](https://larachat.co) - [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel) -->
- [GitHub Discussions](https://github.com/laravel/framework/discussions)
- [Laracasts Forums](https://laracasts.com/discuss)
- [Laravel.io Forums](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="core-development-discussion"></a>
<!-- ## Core Development Discussion -->
## Core Development Discussion

<!-- You may propose new features or improvements of existing Laravel behavior in the Laravel framework repository's [GitHub discussion board](https://github.com/laravel/framework/discussions). If you propose a new feature, please be willing to implement at least some of the code that would be needed to complete the feature. -->
Laravel 프레임워크 저장소의 [GitHub discussion board](https://github.com/laravel/framework/discussions)에서 새 기능이나 기존 Laravel 동작의 개선 사항을 제안할 수 있습니다. 새 기능을 제안한다면, 해당 기능을 완성하는 데 필요한 코드 중 적어도 일부는 직접 구현할 의향이 있어야 합니다.

<!-- Informal discussion regarding bugs, new features, and implementation of existing features takes place in the `#internals` channel of the [Laravel Discord server](https://discord.gg/laravel). Taylor Otwell, the maintainer of Laravel, is typically present in the channel on weekdays from 8am-5pm (UTC-06:00 or America/Chicago), and sporadically present in the channel at other times. -->
버그, 새 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord server](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 관리자인 Taylor Otwell은 보통 평일 오전 8시부터 오후 5시까지(UTC-06:00 또는 America/Chicago) 해당 채널에 있으며, 그 외 시간에도 간헐적으로 채널에 참여합니다.

<a name="which-branch"></a>
<!-- ## Which Branch? -->
## Which Branch?

<!-- **All** bug fixes should be sent to the latest version that supports bug fixes (currently `13.x`). Bug fixes should **never** be sent to the `master` branch unless they fix features that exist only in the upcoming release. -->
**모든** 버그 수정은 버그 수정을 지원하는 최신 버전(현재 `13.x`)으로 보내야 합니다. 다가오는 릴리스에만 존재하는 기능을 수정하는 경우가 아니라면, 버그 수정은 **절대로** `master` 브랜치로 보내서는 안 됩니다.

<!-- **Minor** features that are **fully backward compatible** with the current release may be sent to the latest stable branch (currently `13.x`). -->
현재 릴리스와 **완전히 하위 호환되는** **마이너** 기능은 최신 안정 브랜치(현재 `13.x`)로 보낼 수 있습니다.

<!-- **Major** new features or features with breaking changes should always be sent to the `master` branch, which contains the upcoming release. -->
**메이저** 새 기능이나 호환성을 깨는 변경이 포함된 기능은 항상 다가오는 릴리스를 포함하는 `master` 브랜치로 보내야 합니다.

<a name="compiled-assets"></a>
<!-- ## Compiled Assets -->
## Compiled Assets

<!-- If you are submitting a change that will affect a compiled file, such as most of the files in `resources/css` or `resources/js` of the `laravel/laravel` repository, do not commit the compiled files. Due to their large size, they cannot realistically be reviewed by a maintainer. This could be exploited as a way to inject malicious code into Laravel. In order to defensively prevent this, all compiled files will be generated and committed by Laravel maintainers. -->
`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js`에 있는 대부분의 파일처럼 컴파일된 파일에 영향을 주는 변경 사항을 제출하는 경우, 컴파일된 파일은 커밋하지 마세요. 이러한 파일은 크기가 크기 때문에 관리자가 현실적으로 검토할 수 없습니다. 이 점은 Laravel에 악성 코드를 주입하는 방법으로 악용될 수 있습니다. 이를 방어적으로 방지하기 위해 모든 컴파일된 파일은 Laravel 관리자가 생성하고 커밋합니다.

<a name="ai-generated-contributions"></a>
<!-- ## AI-Generated Contributions -->
## AI-Generated Contributions

<!-- We appreciate every pull request submitted to Laravel. However, contributions that are primarily AI-generated without thoughtful human review and consideration are not acceptable. -->
Laravel에 제출되는 모든 pull request에 감사드립니다. 하지만 충분한 사람의 검토와 고민 없이 주로 AI로 생성된 기여는 허용되지 않습니다.

<!-- If you choose to use AI tools to assist with your contribution, the resulting code **must** be thoroughly reviewed, tested, and understood by you before submitting. -->
기여를 도울 목적으로 AI 도구를 사용하기로 했다면, 제출하기 전에 결과 코드가 **반드시** 본인에 의해 철저히 검토되고, 테스트되며, 이해되어야 합니다.

<!-- Pull request descriptions **must** be written entirely by the contributor. Pull requests with AI-generated descriptions will be closed. -->
풀 리퀘스트 설명은 **반드시** 기여자가 전부 직접 작성해야 합니다. AI가 생성한 설명이 포함된 풀 리퀘스트는 종료됩니다.

<!-- **Mass opening issues or pull requests that are entirely AI-generated will not be tolerated.** Such pull requests will be closed without review, and the contributing user may be blocked from the repository. -->
**전적으로 AI로 생성된 이슈나 pull request를 대량으로 여는 행위는 용납되지 않습니다.** 이러한 pull request는 검토 없이 닫히며, 기여한 사용자는 저장소에서 차단될 수 있습니다.

<!-- We encourage contributors to familiarize themselves with the existing codebase, engage with the community, and submit pull requests that reflect their own understanding and careful consideration of the problem they are solving. -->
기여자들이 기존 코드베이스에 익숙해지고, 커뮤니티와 소통하며, 자신이 해결하려는 문제에 대한 이해와 신중한 고민이 반영된 pull request를 제출하기를 권장합니다.

<a name="security-vulnerabilities"></a>
<!-- ## Security Vulnerabilities -->
## Security Vulnerabilities

<!-- If you discover a security vulnerability within Laravel, please email our security team at <a href="mailto:security@laravel.com">security@laravel.com</a>. All security vulnerabilities will be promptly addressed. -->
Laravel에서 보안 취약점을 발견했다면 <a href="mailto:security@laravel.com">security@laravel.com</a>으로 보안 팀에 이메일을 보내 주세요. 모든 보안 취약점은 신속하게 처리됩니다.

<a name="coding-style"></a>
<!-- ## Coding Style -->
## Coding Style

<!-- Laravel follows the [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) coding standard and the [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) autoloading standard. -->
Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
<!-- ### PHPDoc -->
### PHPDoc

<!-- Below is an example of a valid Laravel documentation block. Note that the `@param` attribute is followed by two spaces, the argument type, two more spaces, and finally the variable name: -->
아래는 유효한 Laravel 문서 블록의 예시입니다. `@param` 속성 뒤에는 공백 두 칸, 인수 타입, 다시 공백 두 칸, 마지막으로 변수명이 온다는 점에 유의하세요.

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

<!-- When the `@param` or `@return` attributes are redundant due to the use of native types, they can be removed: -->
네이티브 타입 사용으로 인해 `@param` 또는 `@return` 속성이 중복된다면 제거할 수 있습니다.

```php
/**
 * Execute the job.
 * [tl! remove]
 * @return void [tl! remove]
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

<!-- However, when the native type is generic, please specify the generic type through the use of the `@param` or `@return` attributes: -->
하지만 네이티브 타입이 제네릭이라면 `@param` 또는 `@return` 속성을 사용해 제네릭 타입을 명시해 주세요.

```php
/**
 * Get the attachments for the message.
 * [tl! add]
 * @return array<int, \Illuminate\Mail\Mailables\Attachment> [tl! add]
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
코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)는 pull request가 병합된 후 스타일 수정 사항을 Laravel 저장소에 자동으로 병합합니다. 이를 통해 우리는 코드 스타일이 아니라 기여 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
<!-- ## Code of Conduct -->
## Code of Conduct

<!-- The Laravel code of conduct is derived from the Ruby code of conduct. Any violations of the code of conduct may be reported to Taylor Otwell (taylor@laravel.com): -->
Laravel 행동 강령은 Ruby 행동 강령에서 파생되었습니다. 행동 강령 위반 사항은 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다.

<div class="content-list" markdown="1">

<!-- - Participants will be tolerant of opposing views. - Participants must ensure that their language and actions are free of personal attacks and disparaging personal remarks. - When interpreting the words and actions of others, participants should always assume good intentions. - Behavior that can be reasonably considered harassment will not be tolerated. -->
- 참가자는 서로 다른 견해를 존중해야 합니다.
- 참가자는 자신의 언어와 행동에 인신공격이나 상대를 폄하하는 개인적 발언이 포함되지 않도록 해야 합니다.
- 다른 사람의 말과 행동을 해석할 때 참가자는 항상 선의의 의도를 전제로 해야 합니다.
- 합리적으로 괴롭힘으로 간주할 수 있는 행동은 용납되지 않습니다.

</div>
