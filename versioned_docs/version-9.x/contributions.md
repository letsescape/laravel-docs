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
Laravel에서는 활발한 협업을 장려하기 위해 단순한 버그 리포트만이 아닌, Pull Request(기능·수정 코드 기여)를 적극적으로 권장합니다. Pull Request는 "Ready for review"(리뷰 준비 완료) 상태로 표시되어야만 검토되며, "draft"(초안) 상태이거나 신규 기능 관련 모든 테스트가 통과하지 않은 경우 검토 대상이 아닙니다. 며칠간 비활성 상태로 남아 있는 draft Pull Request는 자동으로 닫힐 수 있습니다.

<!-- However, if you file a bug report, your issue should contain a title and a clear description of the issue. You should also include as much relevant information as possible and a code sample that demonstrates the issue. The goal of a bug report is to make it easy for yourself - and others - to replicate the bug and develop a fix. -->
버그 리포트를 등록할 경우에는, 반드시 제목과 구체적이고 명확한 설명을 포함해 주세요. 문제를 재현할 수 있는 코드 샘플과 관련 정보를 최대한 자세히 제공해 주셔야 합니다. 버그 리포트의 목적은 작성자 본인과 다른 사람들이 해당 버그를 쉽게 재현하고, 문제를 수정하는 데 도움을 주는 데 있습니다.

<!-- Remember, bug reports are created in the hope that others with the same problem will be able to collaborate with you on solving it. Do not expect that the bug report will automatically see any activity or that others will jump to fix it. Creating a bug report serves to help yourself and others start on the path of fixing the problem. If you want to chip in, you can help out by fixing [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). You must be authenticated with GitHub to view all of Laravel's issues. -->
버그 리포트는 같은 문제를 겪는 다른 사람들이 해결책을 찾아가는 과정에 참여할 수 있도록 남기는 것입니다. 버그 리포트를 올렸다고 해서 즉시 누군가가 해결해 주리라고 기대해서는 안 됩니다. 버그 리포트를 남기는 행위 자체가 본인과 다른 사용자 모두에게 문제 해결의 첫 단추를 제공하는 셈입니다. 직접 버그 수정에 기여하고 싶다면, [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) 중에서 자유롭게 해결을 시도하실 수 있습니다. Laravel의 모든 이슈를 보려면 GitHub 인증이 필요합니다.

<!-- The Laravel source code is managed on GitHub, and there are repositories for each of the Laravel projects: -->
Laravel의 소스 코드는 GitHub에서 관리되고 있으며, 각 프로젝트별로 별도의 저장소가 있습니다.

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
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pint](https://github.com/laravel/pint)
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
- [Laravel Framework](https://github.com/laravel/framework)
- [Laravel Homestead](https://github.com/laravel/homestead)
- [Laravel Homestead Build Scripts](https://github.com/laravel/settler)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Jetstream](https://github.com/laravel/jetstream)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pint](https://github.com/laravel/pint)
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
Laravel의 GitHub 이슈 트래커는 문제 신고와 버그 리포트 용도이며, Laravel 사용법이나 일반적인 지원을 제공하는 곳이 아닙니다. 대신, 아래 커뮤니티 채널들을 이용해 주세요.

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
Laravel의 동작 개선이나 새로운 기능 제안을 원한다면, Laravel 프레임워크 저장소의 [GitHub discussion board](https://github.com/laravel/framework/discussions)에 논의를 남길 수 있습니다. 새로운 기능을 제안할 때는, 해당 기능 구현에 실질적으로 일부라도 직접 코드로 참여할 의향이 있으면 좋습니다.

<!-- Informal discussion regarding bugs, new features, and implementation of existing features takes place in the `#internals` channel of the [Laravel Discord server](https://discord.gg/laravel). Taylor Otwell, the maintainer of Laravel, is typically present in the channel on weekdays from 8am-5pm (UTC-06:00 or America/Chicago), and sporadically present in the channel at other times. -->
버그, 신규 기능, 기존 기능의 구현 등 다양한 비공식 논의는 [Laravel Discord server](https://discord.gg/laravel)의 `#internals` 채널에서 자유롭게 이루어지고 있습니다. Laravel의 관리자인 Taylor Otwell은 평일(UTC-06:00/America/Chicago 기준) 오전 8시~오후 5시에 주로 채널에 있으며, 그 외 시간에도 불규칙하게 접속합니다.

<a name="which-branch"></a>
<!-- ## Which Branch? -->
## Which Branch?

<!-- **All** bug fixes should be sent to the latest version that supports bug fixes (currently `9.x`). Bug fixes should **never** be sent to the `master` branch unless they fix features that exist only in the upcoming release. -->
**모든** 버그 수정은 현재 버그 수정이 적용되는 최신 버전(현재는 `9.x`) 브랜치에 보내야 합니다. 버그 수정은 예외적으로 다음 릴리스 버전에만 존재하는 신규 기능을 고칠 때를 제외하고는, 결코 `master` 브랜치로 직접 보내면 안 됩니다.

<!-- **Minor** features that are **fully backward compatible** with the current release may be sent to the latest stable branch (currently `9.x`). -->
기존 릴리스와 **완전히 하위 호환되는** **마이너**(작은 규모의) 기능 추가는 최신 안정화 브랜치(현재는 `9.x`)에 보낼 수 있습니다.

<!-- **Major** new features or features with breaking changes should always be sent to the `master` branch, which contains the upcoming release. -->
**주요(메이저) 신규 기능** 또는 호환성을 깨뜨릴 수 있는 큰 변경 사항(브레이킹 체인지)은 항상 다음 릴리스가 포함된 `master` 브랜치로만 보내야 합니다.

<a name="compiled-assets"></a>
<!-- ## Compiled Assets -->
## Compiled Assets

<!-- If you are submitting a change that will affect a compiled file, such as most of the files in `resources/css` or `resources/js` of the `laravel/laravel` repository, do not commit the compiled files. Due to their large size, they cannot realistically be reviewed by a maintainer. This could be exploited as a way to inject malicious code into Laravel. In order to defensively prevent this, all compiled files will be generated and committed by Laravel maintainers. -->
`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js` 등, 컴파일이 필요한 파일을 변경하는 경우라면, 수정된 결과물(컴파일된 파일)은 커밋하지 않아야 합니다. 컴파일 파일은 대용량이고, 유지자가 직접 일일이 검토할 수 없기 때문입니다. 악의적으로 변조된 코드를 심을 위험을 방지하기 위해 보호 차원에서, 모든 컴파일 파일은 Laravel 유지자가 직접 생성해서 커밋하게 되어 있습니다.

<a name="security-vulnerabilities"></a>
<!-- ## Security Vulnerabilities -->
## Security Vulnerabilities

<!-- If you discover a security vulnerability within Laravel, please send an email to Taylor Otwell at <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. All security vulnerabilities will be promptly addressed. -->
Laravel에서 보안 취약점을 발견한 경우, Taylor Otwell에게 이메일로(<a href="mailto:taylor@laravel.com">taylor@laravel.com</a>) 알려주세요. 접수된 보안 이슈는 신속하게 처리됩니다.

<a name="coding-style"></a>
<!-- ## Coding Style -->
## Coding Style

<!-- Laravel follows the [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) coding standard and the [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) autoloading standard. -->
Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준, 그리고 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 오토로딩 표준을 따릅니다.

<a name="phpdoc"></a>
<!-- ### PHPDoc -->
### PHPDoc

<!-- Below is an example of a valid Laravel documentation block. Note that the `@param` attribute is followed by two spaces, the argument type, two more spaces, and finally the variable name: -->
아래는 Laravel에서 사용하는 올바른 문서화 블록(PHPDoc) 예시입니다. `@param` 속성 뒤에 두 칸의 공백, 인수 타입, 다시 두 칸의 공백, 그리고 변수명이 이어지는 방식임을 참고하세요.

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
    //
}
```

<a name="styleci"></a>
<!-- ### StyleCI -->
### StyleCI

<!-- Don't worry if your code styling isn't perfect! [StyleCI](https://styleci.io/) will automatically merge any style fixes into the Laravel repository after pull requests are merged. This allows us to focus on the content of the contribution and not the code style. -->
코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)가 Pull Request가 머지된 이후 자동으로 스타일 정리를 해줍니다. 덕분에 기여자는 코드 내용에만 집중하면 됩니다.

<a name="code-of-conduct"></a>
<!-- ## Code of Conduct -->
## Code of Conduct

<!-- The Laravel code of conduct is derived from the Ruby code of conduct. Any violations of the code of conduct may be reported to Taylor Otwell (taylor@laravel.com): -->
Laravel의 행동 강령은 Ruby 커뮤니티의 행동 강령에서 유래되었습니다. 행동 강령을 위반하는 사례가 발견되면 Taylor Otwell(taylor@laravel.com)에게 신고하실 수 있습니다.

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should always assume good intentions.
- Behavior that can be reasonably considered harassment will not be tolerated.
-->
- 참가자는 서로의 반대 의견에 관용적인 태도를 지녀야 합니다.
- 참가자는 언어나 행동에서 개인에 대한 공격이나 경멸적 발언을 삼가야 합니다.
- 타인의 말과 행동을 해석할 때 항상 선의(善意)를 전제로 해야 합니다.
- 괴롭힘으로 간주할 수 있는 행동은 용납되지 않습니다.

<!-- </div> -->
</div>
