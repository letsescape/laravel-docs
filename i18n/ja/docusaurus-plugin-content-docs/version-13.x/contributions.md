# 貢献ガイド (Contribution Guide)

- [バグレポート](#bug-reports)
- [サポートに関する質問](#support-questions)
- [コア開発のディスカッション](#core-development-discussion)
- [どの支店ですか？](#which-branch)
- [コンパイルされたアセット](#compiled-assets)
- [AI によって生成された貢献](#ai-generated-contributions)
- [セキュリティの脆弱性](#security-vulnerabilities)
- [コーディングスタイル](#coding-style)
    - [PHPDoc](#phpdoc)
    - [StyleCI](#styleci)
- [行動規範](#code-of-conduct)

<a name="bug-reports"></a>
## バグレポート (Bug Reports)

積極的なコラボレーションを促進するために、Laravel ではバグレポートだけでなくプルリクエストを強く推奨しています。プル リクエストは、(「ドラフト」状態ではなく) 「レビュー準備完了」としてマークされ、新機能のすべてのテストが合格した場合にのみレビューされます。 「ドラフト」状態のまま残された非アクティブなプル リクエストは、数日後に閉じられます。

ただし、バグレポートを提出する場合は、問題のタイトルと明確な説明を含める必要があります。また、できるだけ多くの関連情報と、問題を示すコード サンプルも含める必要があります。バグ レポートの目的は、自分自身や他の人がバグを再現し、修正を開発しやすくすることです。

バグ レポートは、同じ問題を抱えている他の人が協力して解決できることを期待して作成されることに注意してください。バグレポートに何らかのアクティビティが自動的に表示されることや、他の人がそれを修正するために飛びつくことを期待しないでください。バグ レポートを作成すると、自分自身や他の人が問題解決の道を歩み始めるのに役立ちます。協力したい場合は、[問題トラッカーにリストされているバグ](https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abug+user%3Alaravel) を修正することで支援できます。 Laravel の問題をすべて表示するには、GitHub で認証される必要があります。

Laravel の使用中に不適切な DocBlock、PHPStan、または IDE の警告に気付いた場合は、GitHub の問題を作成しないでください。代わりに、問題を修正するにはプルリクエストを送信してください。

Laravel のソース コードは GitHub で管理されており、Laravel プロジェクトごとにリポジトリがあります。

<div class="content-list" markdown="1">

- [Laravelアプリケーション](https://github.com/laravel/laravel)
- [Laravelアート](https://github.com/laravel/art)
- [Laravelブースト](https://github.com/laravel/boost)
- [Laravelのドキュメント](https://github.com/laravel/docs)
- [Laravel Dusk](https://github.com/laravel/dusk)
- [Laravel Cashier Stripe](https://github.com/laravel/cashier)
- [Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle)
- [Laravel Echo](https://github.com/laravel/echo)
- [Laravel特使](https://github.com/laravel/envoy)
- [Laravel Folio](https://github.com/laravel/folio)
- [Laravelフレームワーク](https://github.com/laravel/framework)
- [Laravel Horizon](https://github.com/laravel/horizon)
- [Laravel Passport](https://github.com/laravel/passport)
- [Laravel Pennant](https://github.com/laravel/pennant)
- [LaravelPint](https://github.com/laravel/pint)
- [Laravelプロンプト](https://github.com/laravel/prompts)
- [Laravel Reverb](https://github.com/laravel/reverb)
- [Laravel Sail](https://github.com/laravel/sail)
- [Laravel Sanctum](https://github.com/laravel/sanctum)
- [Laravel Scout](https://github.com/laravel/scout)
- [Laravel Socialite](https://github.com/laravel/socialite)
- [Laravel Telescope](https://github.com/laravel/telescope)
- [Laravel Livewire スターターキット](https://github.com/laravel/livewire-starter-kit)
- [Laravel React スターターキット](https://github.com/laravel/react-starter-kit)
- [Laravel Svelte スターター キット](https://github.com/laravel/svelte-starter-kit)
- [Laravel Vue スターターキット](https://github.com/laravel/vue-starter-kit)

</div>

<a name="support-questions"></a>
## サポートに関する質問 (Support Questions)

Laravel の GitHub 問題トラッカーは、Laravel のヘルプやサポートを提供することを目的としたものではありません。代わりに、次のいずれかのチャネルを使用してください。

<div class="content-list" markdown="1">

- [GitHub ディスカッション](https://github.com/laravel/framework/discussions)
- [ララキャストのフォーラム](https://laracasts.com/discuss)
- [Laravel.io フォーラム](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [Discord](https://discord.gg/laravel)
- [Larachat](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="core-development-discussion"></a>
## コア開発のディスカッション (Core Development Discussion)

Laravel フレームワーク リポジトリの [GitHub ディスカッション掲示板](https://github.com/laravel/framework/discussions) で、新しい機能や既存の Laravel 動作の改善を提案できます。新しい機能を提案する場合は、その機能を完成させるために必要なコードの少なくとも一部を実装してください。

バグ、新機能、既存機能の実装に関する非公式のディスカッションは、[Laravel Discordサーバー](https://discord.gg/laravel) の `#internals` チャネルで行われます。 Laravel のメンテナである Taylor Otwell は通常、平日の午前 8 時から午後 5 時 (UTC-06:00 またはアメリカ/シカゴ) までチャネルに存在し、それ以外の時間帯にも散発的にチャネルに存在します。

<a name="which-branch"></a>
## どの支店ですか？ (Which Branch?)

**すべて**のバグ修正は、バグ修正をサポートする最新バージョン (現在 `13.x`) に送信する必要があります。バグ修正は、今後のリリースにのみ存在する機能を修正するものでない限り、`master` ブランチには**決して**送信しないでください。

現在のリリースと **完全に下位互換性がある**マイナー**機能は、最新の安定したブランチ (現在 `13.x`) に送信される場合があります。

**主要な**新機能または重大な変更を伴う機能は、次のリリースが含まれる `master` ブランチに常に送信する必要があります。

<a name="compiled-assets"></a>
## コンパイルされたアセット (Compiled Assets)

`laravel/laravel` リポジトリの `resources/css` または `resources/js` 内のほとんどのファイルなど、コンパイル済みファイルに影響を与える変更を送信する場合は、コンパイル済みファイルをコミットしないでください。サイズが大きいため、現実的にはメンテナがレビューすることはできません。これは、悪意のあるコードを Laravel に挿入する方法として悪用される可能性があります。これを防御的に防ぐために、すべてのコンパイル済みファイルは Laravel メンテナによって生成およびコミットされます。

<a name="ai-generated-contributions"></a>
## AI によって生成された貢献 (AI-Generated Contributions)

Laravel に送信されたすべてのプルリクエストに感謝します。ただし、人間による思慮深いレビューや検討を経ずに主に AI によって生成された投稿は受け入れられません。

AI ツールを使用して貢献を支援することを選択した場合、結果として得られるコードは、提出する前に**徹底的にレビュー、テストされ、理解されている必要があります**。

**完全に AI によって生成された問題やプル リクエストを大量に開くことは許容されません。** このようなプル リクエストはレビューなしで閉じられ、投稿したユーザーはリポジトリからブロックされる場合があります。

コントリビューターには、既存のコードベースに慣れ、コミュニティに参加し、解決しようとしている問題についての自身の理解と慎重な検討を反映したプル リクエストを送信することをお勧めします。

<a name="security-vulnerabilities"></a>
## セキュリティの脆弱性 (Security Vulnerabilities)

Laravel 内でセキュリティ脆弱性を発見した場合は、Taylor Otwell (<a href="mailto:taylor@laravel.com">taylor@laravel.com</a>) へメールを送信してください。すべてのセキュリティ脆弱性は速やかに対応されます。

<a name="coding-style"></a>
## コーディングスタイル (Coding Style)

Laravel は、[PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) コーディング標準と [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) オートロード標準に従っています。

<a name="phpdoc"></a>
### PHPDoc

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

`@param` 属性または `@return` 属性がネイティブ タイプの使用により冗長である場合、それらは削除できます。

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

ただし、ネイティブ タイプがジェネリックの場合は、`@param` または `@return` 属性を使用してジェネリック タイプを指定してください。

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
### スタイルCI

コードのスタイルが完璧でなくても心配する必要はありません。 [StyleCI](https://styleci.io/) は、プルリクエストがマージされた後、スタイル修正を自動的に Laravel リポジトリにマージします。これにより、コード スタイルではなく、投稿の内容に集中できるようになります。

<a name="code-of-conduct"></a>
## 行動規範 (Code of Conduct)

Laravel の行動規範は、Ruby の行動規範から派生しています。行動規範の違反は、Taylor Otwell (taylor@laravel.com) に報告される場合があります。

<div class="content-list" markdown="1">

- 参加者は反対意見にも寛容になります。
- 参加者は、自分の言語や行動に個人攻撃や個人を軽蔑する発言がないことを確認する必要があります。
- 他者の言葉や行動を解釈するとき、参加者は常に善意を想定する必要があります。
- ハラスメントと合理的にみなされる行為は容認されません。

</div>

