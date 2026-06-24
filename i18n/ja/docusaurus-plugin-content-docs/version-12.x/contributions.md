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
積極的なコラボレーションを促進するために、Laravel ではバグレポートだけでなくプルリクエストを強く推奨しています。プル リクエストは、(「ドラフト」状態ではなく) 「レビュー準備完了」としてマークされ、新機能のすべてのテストが合格した場合にのみレビューされます。 「ドラフト」状態のまま残された非アクティブなプル リクエストは、数日後に閉じられます。

<!-- However, if you file a bug report, your issue should contain a title and a clear description of the issue. You should also include as much relevant information as possible and a code sample that demonstrates the issue. The goal of a bug report is to make it easy for yourself - and others - to replicate the bug and develop a fix. -->
ただし、バグレポートを提出する場合は、問題のタイトルと明確な説明を含める必要があります。また、できるだけ多くの関連情報と、問題を示すコード サンプルも含める必要があります。バグ レポートの目的は、自分自身や他の人がバグを再現し、修正を開発しやすくすることです。

<!-- Remember, bug reports are created in the hope that others with the same problem will be able to collaborate with you on solving it. Do not expect that the bug report will automatically see any activity or that others will jump to fix it. Creating a bug report serves to help yourself and others start on the path of fixing the problem. If you want to chip in, you can help out by fixing [any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel). You must be authenticated with GitHub to view all of Laravel's issues. -->
バグ レポートは、同じ問題を抱えている他の人が協力して解決できることを期待して作成されることに注意してください。バグレポートに何らかのアクティビティが自動的に表示されることや、他の人がそれを修正するために飛びつくことを期待しないでください。バグ レポートを作成すると、自分自身や他の人が問題解決の道を歩み始めるのに役立ちます。協力したい場合は、[any bugs listed in our issue trackers](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) を修正することで支援できます。 Laravel の問題をすべて表示するには、GitHub で認証される必要があります。

<!-- If you notice improper DocBlock, PHPStan, or IDE warnings while using Laravel, do not create a GitHub issue. Instead, please submit a pull request to fix the problem. -->
Laravel の使用中に不適切な DocBlock、PHPStan、または IDE の警告に気付いた場合は、GitHub の問題を作成しないでください。代わりに、問題を修正するにはプルリクエストを送信してください。

<!-- The Laravel source code is managed on GitHub, and there are repositories for each of the Laravel projects: -->
Laravel のソース コードは GitHub で管理されており、Laravel プロジェクトごとにリポジトリがあります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
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
-->
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

<!-- </div> -->
</div>

<a name="support-questions"></a>
<!-- ## Support Questions -->
## Support Questions

<!-- Laravel's GitHub issue trackers are not intended to provide Laravel help or support. Instead, use one of the following channels: -->
Laravel の GitHub 問題トラッカーは、Laravel のヘルプやサポートを提供することを目的としたものではありません。代わりに、次のいずれかのチャネルを使用してください。

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
Laravel フレームワーク リポジトリの [GitHub discussion board](https://github.com/laravel/framework/discussions) で、新しい機能や既存の Laravel 動作の改善を提案できます。新しい機能を提案する場合は、その機能を完成させるために必要なコードの少なくとも一部を実装してください。

<!-- Informal discussion regarding bugs, new features, and implementation of existing features takes place in the `#internals` channel of the [Laravel Discord server](https://discord.gg/laravel). Taylor Otwell, the maintainer of Laravel, is typically present in the channel on weekdays from 8am-5pm (UTC-06:00 or America/Chicago), and sporadically present in the channel at other times. -->
バグ、新機能、既存機能の実装に関する非公式のディスカッションは、[Laravel Discord server](https://discord.gg/laravel) の `#internals` チャネルで行われます。 Laravel のメンテナである Taylor Otwell は通常、平日の午前 8 時から午後 5 時 (UTC-06:00 またはアメリカ/シカゴ) までチャネルに存在し、それ以外の時間帯にも散発的にチャネルに存在します。

<a name="which-branch"></a>
<!-- ## Which Branch? -->
## Which Branch?

<!-- **All** bug fixes should be sent to the latest version that supports bug fixes (currently `12.x`). Bug fixes should **never** be sent to the `master` branch unless they fix features that exist only in the upcoming release. -->
**すべて**のバグ修正は、バグ修正をサポートする最新バージョン (現在 `12.x`) に送信する必要があります。バグ修正は、今後のリリースにのみ存在する機能を修正するものでない限り、`master` ブランチには**決して**送信しないでください。

<!-- **Minor** features that are **fully backward compatible** with the current release may be sent to the latest stable branch (currently `12.x`). -->
現在のリリースと**完全に下位互換性がある**、**マイナー**機能は、最新の安定したブランチ (現在 `12.x`) に送信される場合があります。

<!-- **Major** new features or features with breaking changes should always be sent to the `master` branch, which contains the upcoming release. -->
**主要な**新機能または重大な変更を伴う機能は、次のリリースが含まれる `master` ブランチに常に送信する必要があります。

<a name="compiled-assets"></a>
<!-- ## Compiled Assets -->
## Compiled Assets

<!-- If you are submitting a change that will affect a compiled file, such as most of the files in `resources/css` or `resources/js` of the `laravel/laravel` repository, do not commit the compiled files. Due to their large size, they cannot realistically be reviewed by a maintainer. This could be exploited as a way to inject malicious code into Laravel. In order to defensively prevent this, all compiled files will be generated and committed by Laravel maintainers. -->
`laravel/laravel` リポジトリの `resources/css` または `resources/js` 内のほとんどのファイルなど、コンパイル済みファイルに影響を与える変更を送信する場合は、コンパイル済みファイルをコミットしないでください。サイズが大きいため、現実的にはメンテナがレビューすることはできません。これは、悪意のあるコードを Laravel に挿入する方法として悪用される可能性があります。これを防御的に防ぐために、すべてのコンパイル済みファイルは Laravel メンテナによって生成およびコミットされます。

<a name="ai-generated-contributions"></a>
<!-- ## AI-Generated Contributions -->
## AI-Generated Contributions

<!-- We appreciate every pull request submitted to Laravel. However, contributions that are primarily AI-generated without thoughtful human review and consideration are not acceptable. -->
Laravel に送信されたすべてのプルリクエストに感謝します。ただし、人間による思慮深いレビューや検討を経ずに主に AI によって生成された投稿は受け入れられません。

<!-- If you choose to use AI tools to assist with your contribution, the resulting code **must** be thoroughly reviewed, tested, and understood by you before submitting. -->
AI ツールを使用して貢献を支援することを選択した場合、結果として得られるコードは、提出する前に**徹底的にレビュー、テストされ、理解されている必要があります**。

<!-- **Mass opening issues or pull requests that are entirely AI-generated will not be tolerated.** Such pull requests will be closed without review, and the contributing user may be blocked from the repository. -->
**完全に AI によって生成された問題やプル リクエストを大量に開くことは許容されません。** このようなプル リクエストはレビューなしで閉じられ、投稿したユーザーはリポジトリからブロックされる場合があります。

<!-- We encourage contributors to familiarize themselves with the existing codebase, engage with the community, and submit pull requests that reflect their own understanding and careful consideration of the problem they are solving. -->
コントリビューターには、既存のコードベースに慣れ、コミュニティに参加し、解決しようとしている問題についての自身の理解と慎重な検討を反映したプル リクエストを送信することをお勧めします。

<a name="security-vulnerabilities"></a>
<!-- ## Security Vulnerabilities -->
## Security Vulnerabilities

<!-- If you discover a security vulnerability within Laravel, please send an email to Taylor Otwell at <a href="mailto:taylor@laravel.com">taylor@laravel.com</a>. All security vulnerabilities will be promptly addressed. -->
Laravel 内でセキュリティ脆弱性を発見した場合は、Taylor Otwell (<a href="mailto:taylor@laravel.com">taylor@laravel.com</a>) へメールを送信してください。すべてのセキュリティ脆弱性は速やかに対応されます。

<a name="coding-style"></a>
<!-- ## Coding Style -->
## Coding Style

<!-- Laravel follows the [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) coding standard and the [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) autoloading standard. -->
Laravel は、[PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) コーディング標準と [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) オートロード標準に従っています。

<a name="phpdoc"></a>
<!-- ### PHPDoc -->
### PHPDoc

<!-- Below is an example of a valid Laravel documentation block. Note that the `@param` attribute is followed by two spaces, the argument type, two more spaces, and finally the variable name: -->
以下は、有効な Laravel ドキュメント ブロックの例です。 `@param` 属性の後には 2 つのスペース、引数の型、さらに 2 つのスペース、そして最後に変数名が続くことに注意してください。

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
`@param` 属性または `@return` 属性がネイティブ タイプの使用により冗長である場合、それらは削除できます。

```php
/**
 * Execute the job.
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}
```

<!-- However, when the native type is generic, please specify the generic type through the use of the `@param` or `@return` attributes: -->
ただし、ネイティブ タイプがジェネリックの場合は、`@param` または `@return` 属性を使用してジェネリック タイプを指定してください。

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
<!-- ### StyleCI -->
### StyleCI

<!-- Don't worry if your code styling isn't perfect! [StyleCI](https://styleci.io/) will automatically merge any style fixes into the Laravel repository after pull requests are merged. This allows us to focus on the content of the contribution and not the code style. -->
コードのスタイルが完璧でなくても心配する必要はありません。 [StyleCI](https://styleci.io/) は、プルリクエストがマージされた後、スタイル修正を自動的に Laravel リポジトリにマージします。これにより、コード スタイルではなく、投稿の内容に集中できるようになります。

<a name="code-of-conduct"></a>
<!-- ## Code of Conduct -->
## Code of Conduct

<!-- The Laravel code of conduct is derived from the Ruby code of conduct. Any violations of the code of conduct may be reported to Taylor Otwell (taylor@laravel.com): -->
Laravel の行動規範は、Ruby の行動規範から派生しています。行動規範の違反は、Taylor Otwell (taylor@laravel.com) に報告される場合があります。

<!-- <div class="content-list" markdown="1"> -->
<div class="content-list" markdown="1">

<!--
- Participants will be tolerant of opposing views.
- Participants must ensure that their language and actions are free of personal attacks and disparaging personal remarks.
- When interpreting the words and actions of others, participants should always assume good intentions.
- Behavior that can be reasonably considered harassment will not be tolerated.
-->
- 参加者は反対意見にも寛容になります。
- 参加者は、自分の言語や行動に個人攻撃や個人を軽蔑する発言がないことを確認する必要があります。
- 他者の言葉や行動を解釈するとき、参加者は常に善意を想定する必要があります。
- ハラスメントと合理的にみなされる行為は容認されません。

<!-- </div> -->
</div>

