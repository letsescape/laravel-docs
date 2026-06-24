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
Laravel은 적극적인 협업을 위해, 단순한 버그 리포트 뿐만 아니라 풀 리퀘스트(Pull Request)를 보내는 것을 강력하게 권장합니다. 풀 리퀘스트를 리뷰받으려면 반드시 "ready for review"(검토 준비 완료) 상태여야 하며, "draft"(초안) 상태에서는 리뷰되지 않습니다. 새로운 기능을 추가하는 경우, 모든 테스트가 통과해야만 리뷰가 진행됩니다. 오랜 기간 동안 "draft" 상태로 비활성화되어 있는 풀 리퀘스트는 며칠 후에 닫힐 수 있습니다.

<!-- However, if you file a bug report, your issue should contain a title and a clear description of the issue. You should also include as much relevant information as possible and a code sample that demonstrates the issue. The goal of a bug report is to make it easy for yourself - and others - to replicate the bug and develop a fix. -->
그럼에도 불구하고 버그 리포트를 제출할 때에는, 이슈 제목과 문제에 대한 명확한 설명을 포함해야 합니다. 또한 문제를 재현할 수 있도록 관련 정보와 문제를 보여주는 코드 샘플을 최대한 자세히 첨부하는 것이 좋습니다. 버그 리포트의 목적은 본인은 물론 다른 사람들이 문제를 쉽게 재현하고 해결 방법을 찾을 수 있도록 돕는 것입니다.

<!-- Remember, bug reports are created in the hope that others with the same problem will be able to collaborate with you on solving it. Do not expect that the bug report will automatically see any activity or that others will jump to fix it. Creating a bug report serves to help yourself and others start on the path of fixing the problem. If you want to chip in, you can help out by fixing [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). You must be authenticated with GitHub to view all of Laravel's issues. -->
버그 리포트는 비슷한 문제를 겪는 다른 사람들이 함께 해결책을 찾을 수 있도록 만들기 위한 것입니다. 버그 리포트를 작성한다고 해서 반드시 즉시 반응이 오거나 바로 누군가가 고쳐주리라 기대하지 마십시오. 버그 리포트는 문제 해결의 첫 걸음을 시작하는 데 도움을 주고자 작성하는 것입니다. 직접 기여하고 싶다면 [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중에서 직접 수정에 참여할 수도 있습니다. Laravel의 모든 이슈를 확인하려면 GitHub에 로그인해야 합니다.

<!-- If you notice improper DocBlock, PHPStan, or IDE warnings while using Laravel, do not create a GitHub issue. Instead, please submit a pull request to fix the problem. -->
Laravel을 사용하면서 DocBlock, PHPStan, 또는 IDE 경고 등의 잘못된 부분을 발견한다면, 별도의 GitHub 이슈를 만들지 말고, 해당 문제를 직접 수정 후 풀 리퀘스트로 보내주십시오.

<!-- The Laravel source code is managed on GitHub, and there are repositories for each of the Laravel projects: -->
Laravel의 소스코드는 GitHub에서 관리되고 있으며, 다양한 Laravel 프로젝트별로 각각의 저장소가 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Website](https://github.com/laravel/laravel.com-next)
-->
- [Laravel Application](https://github.com/laravel/laravel)
- [Laravel Art](https://github.com/laravel/art)
- [Laravel Documentation](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel Envoy](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [Laravel Pint](https://github.com/laravel/pint)
- [Laravel Prompts](https://github.com/laravel/prompts)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Website](https://github.com/laravel/laravel.com-next)

<!-- </div> -->
</div>

<a name="support-questions"></a>
<!-- ## Support Questions -->
## Support Questions

<!-- Laravel's GitHub issue trackers are not intended to provide Laravel help or support. Instead, use one of the following channels: -->
Laravel의 GitHub 이슈 트래커는 Laravel 사용 관련 질문이나 지원 요청을 위한 공간이 아닙니다. 아래의 공식 지원 채널 중 하나를 이용해 주세요.

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
새로운 기능 제안이나 기존 Laravel 동작의 개선 아이디어가 있다면, Laravel 프레임워크 저장소의 [GitHub discussion board](https://github.com/laravel/framework/discussions)에 제안해 주시기 바랍니다. 새로운 기능을 제안할 때에는 최소한 일부 구현 코드를 직접 작성할 의사가 있어야 합니다.

<!-- Informal discussion regarding bugs, new features, and implementation of existing features takes place in the `#internals` channel of the [Laravel Discord server](https://discord.gg/laravel). Taylor Otwell, the maintainer of Laravel, is typically present in the channel on weekdays from 8am-5pm (UTC-06:00 or America/Chicago), and sporadically present in the channel at other times. -->
버그, 신규 기능, 기존 기능 구현에 대한 비공식 논의는 [Laravel Discord server](https://discord.gg/laravel)의 `#internals` 채널에서 이루어집니다. Laravel의 메인테이너인 Taylor Otwell은 보통 미국 중부 시간대(UTC-06:00 또는 America/Chicago 기준)로 평일 오전 8시부터 오후 5시까지 채널에 상주하며, 그 외 시간에도 가끔 접속합니다.

<a name="which-branch"></a>
<!-- ## Which Branch? -->
## Which Branch?

<!-- **All** bug fixes should be sent to the latest version that supports bug fixes (currently `10.x`). Bug fixes should **never** be sent to the `master` branch unless they fix features that exist only in the upcoming release. -->
**모든** 버그 수정은 현재 버그 수정을 지원하는 최신 버전(현재는 `10.x`) 브랜치로 보내야 합니다. 버그 수정은, 다가오는 릴리스에만 존재하는 기능을 고치는 경우가 아닌 한, **절대로** `master` 브랜치로 보내지 마십시오.

<!-- **Minor** features that are **fully backward compatible** with the current release may be sent to the latest stable branch (currently `10.x`). -->
**완전히 하위 호환성**을 유지하는 **경미한** 기능 추가는 최신 안정 브랜치(현재는 `10.x`)로 보낼 수 있습니다.

<!-- **Major** new features or features with breaking changes should always be sent to the `master` branch, which contains the upcoming release. -->
**주요** 새로운 기능, 또는 하위 호환성이 깨지는 변경사항이 있는 기능은 항상 `master` 브랜치(향후 릴리스를 위한 브랜치)로 보내야 합니다.

<a name="compiled-assets"></a>
<!-- ## Compiled Assets -->
## Compiled Assets

<!-- If you are submitting a change that will affect a compiled file, such as most of the files in `resources/css` or `resources/js` of the `laravel/laravel` repository, do not commit the compiled files. Due to their large size, they cannot realistically be reviewed by a maintainer. This could be exploited as a way to inject malicious code into Laravel. In order to defensively prevent this, all compiled files will be generated and committed by Laravel maintainers. -->
`laravel/laravel` 저장소의 `resources/css`나 `resources/js`에 있는 대부분의 컴파일된 파일에 변경사항이 생기는 커밋을 제출할 경우, **컴파일된 파일은 절대로 커밋하지 마십시오**. 이러한 파일은 용량이 커서 메인테이너가 현실적으로 리뷰하기 어렵습니다. 만약 커밋된다면 악의적인 코드를 Laravel에 삽입하는 수단으로 악용될 수 있습니다. 이를 방지하기 위해, 모든 컴파일된 파일은 Laravel 메인테이너가 직접 생성 및 커밋합니다.

<a name="security-vulnerabilities"></a>
<!-- ## Security Vulnerabilities -->
## Security Vulnerabilities

<!-- If you discover a security vulnerability within Laravel, please send an email to Taylor Otwell at <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. All security vulnerabilities will be promptly addressed. -->
Laravel에서 보안 취약점을 발견했을 경우, Taylor Otwell에게 <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>으로 이메일을 보내주시기 바랍니다. 모든 보안 취약점은 신속하게 처리될 것입니다.

<a name="coding-style"></a>
<!-- ## Coding Style -->
## Coding Style

<!-- Laravel follows the [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) coding standard and the [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) autoloading standard. -->
Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
<!-- ### PHPDoc -->
### PHPDoc

<!-- Below is an example of a valid Laravel documentation block. Note that the `@param` attribute is followed by two spaces, the argument type, two more spaces, and finally the variable name: -->
아래는 Laravel에서 올바른 문서화 블록의 예시입니다. `@param` 속성 뒤에 공백 2개, 인수 타입, 공백 2개, 마지막으로 변수 이름이 오오는 것에 유의하세요.

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
네이티브 타입으로 되어 있어서 `@param` 또는 `@return` 속성이 중복되는 경우, 해당 속성은 제거할 수 있습니다.

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
하지만 네이티브 타입이 제네릭인 경우에는, 반드시 `@param` 또는 `@return` 속성을 이용해 제네릭 타입을 명시해 주어야 합니다.

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
코드 스타일이 완벽하지 않아도 너무 걱정하실 필요 없습니다! [StyleCI](https://styleci.io/)가 풀 리퀘스트가 병합된 이후, Laravel 저장소에 자동으로 코드 스타일을 맞춰줍니다. 덕분에 기여 내용에 더 집중할 수 있고, 코드 스타일 자체에는 신경을 덜 쓸 수 있습니다.

<a name="code-of-conduct"></a>
<!-- ## Code of Conduct -->
## Code of Conduct

<!-- The Laravel code of conduct is derived from the Ruby code of conduct. Any violations of the code of conduct may be reported to Taylor Otwell (taylor@laravel.com): -->
Laravel의 행동 강령은 Ruby 커뮤니티의 행동 강령에서 영감을 받았습니다. 행동 강령을 위반하는 경우 Taylor Otwell(taylor@laravel.com)에게 신고할 수 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should always assume good intentions.
- Behavior that can be reasonably considered harassment will not be tolerated.
-->
- 참가자는 서로의 상반된 견해를 관용적으로 받아들여야 합니다.
- 참가자는 언행이 개인 공격이나 비방이 되지 않도록 스스로 조심해야 합니다.
- 타인의 언행을 해석할 때는 항상 선의로 받아들이도록 노력해야 합니다.
- 상식적으로 괴롭힘(하라스먼트)으로 받아들여질 수 있는 모든 행위는 절대로 용인하지 않습니다.

<!-- </div> -->
</div>
