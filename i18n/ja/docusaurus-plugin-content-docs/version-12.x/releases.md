<!-- # Release Notes -->
# Release Notes

- [Versioning Scheme](#versioning-scheme)
- [Support Policy](#support-policy)
- [Laravel 12](#laravel-12)

<a name="versioning-scheme"></a>
<!-- ## Versioning Scheme -->
## Versioning Scheme

<!-- Laravel and its other first-party packages follow [Semantic Versioning](https://semver.org). Major framework releases are released every year (~Q1), while minor and patch releases may be released as often as every week. Minor and patch releases should **never** contain breaking changes. -->
Laravel とその他のファーストパーティ パッケージは [Semantic Versioning](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

<!-- When referencing the Laravel framework or its components from your application or package, you should always use a version constraint such as `^12.0`, since major releases of Laravel do include breaking changes. However, we strive to always ensure you may update to a new major release in one day or less. -->
Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^12.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
<!-- #### Named Arguments -->
#### Named Arguments

<!-- [Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) are not covered by Laravel's backwards compatibility guidelines. We may choose to rename function arguments when necessary in order to improve the Laravel codebase. Therefore, using named arguments when calling Laravel methods should be done cautiously and with the understanding that the parameter names may change in the future. -->
[Named arguments](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
<!-- ## Support Policy -->
## Support Policy

<!-- For all Laravel releases, bug fixes are provided for 18 months and security fixes are provided for 2 years. For all additional libraries, only the latest major release receives bug fixes. In addition, please review the database versions [supported by Laravel](/docs/12.x/database#introduction). -->
すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。すべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [supported by Laravel](/docs/12.x/database#introduction) を確認してください。

<!-- <div class="overflow-auto"> -->
<div class="overflow-auto">

| バージョン | PHP(*)   | リリース             | バグ修正まで     | セキュリティ修正の期限 |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日    | 2025 年 2 月 4 日   |
| 11      | 8.2～8.4 | 2024 年 3 月 12 日    | 2025 年 9 月 3 日 | 2026 年 3 月 12 日     |
| 12      | 8.2～8.5 | 2025 年 2 月 24 日 | 2026 年 8 月 13 日   | 2027 年 2 月 24 日  |
| 13      | 8.3～8.5 | 2026 年第 1 四半期             | 2027 年第 3 四半期             | 2028 年第 1 四半期              |

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
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

<!-- (*) Supported PHP versions -->
(*) サポートされている PHP バージョン

<a name="laravel-12"></a>
<!-- ## Laravel 12 -->
## Laravel 12

<!-- Laravel 12 continues the improvements made in Laravel 11.x by updating upstream dependencies and introducing new starter kits for React, Svelte, Vue, and Livewire, including the option of using [WorkOS AuthKit](https://authkit.com) for user authentication. The WorkOS variant of our starter kits offers social authentication, passkeys, and SSO support. -->
Laravel 12 は、アップストリームの依存関係を更新し、ユーザー認証に [WorkOS AuthKit](https://authkit.com) を使用するオプションを含む React、Svelte、Vue、Livewire の新しいスターター キットを導入することにより、Laravel 11.x で行われた改善を継続しています。スターター キットの WorkOS バリアントは、ソーシャル認証、パスキー、および SSO サポートを提供します。

<a name="minimal-breaking-changes"></a>
<!-- ### Minimal Breaking Changes -->
### Minimal Breaking Changes

<!-- Much of our focus during this release cycle has been minimizing breaking changes. Instead, we have dedicated ourselves to shipping continuous quality-of-life improvements throughout the year that do not break existing applications. -->
このリリース サイクルでは、重大な変更を最小限に抑えることに重点を置いています。その代わりに、私たちは既存のアプリケーションを壊すことなく、年間を通して継続的に生活の質を向上させることに専念してきました。

<!-- Therefore, the Laravel 12 release is a relatively minor "maintenance release" in order to upgrade existing dependencies. In light of this, most Laravel applications may upgrade to Laravel 12 without changing any application code. -->
したがって、Laravel 12 リリースは、既存の依存関係をアップグレードするための比較的マイナーな「メンテナンス リリース」です。これを考慮すると、ほとんどの Laravel アプリケーションは、アプリケーション コードを変更せずに Laravel 12 にアップグレードできます。

<a name="new-application-starter-kits"></a>
<!-- ### New Application Starter Kits -->
### New Application Starter Kits

<!-- Laravel 12 introduces new [application starter kits](/docs/12.x/starter-kits) for React, Svelte, Vue, and Livewire. The React, Svelte, and Vue starter kits utilize Inertia 2, TypeScript, [shadcn/ui](https://ui.shadcn.com), and Tailwind, while the Livewire starter kits utilize the Tailwind-based [Flux UI](https://fluxui.dev) component library and Laravel Volt. -->
Laravel 12 では、React、Svelte、Vue、Livewire 用の新しい [application starter kits](/docs/12.x/starter-kits) が導入されています。 React、Svelte、Vue スターター キットは Inertia 2、TypeScript、[shadcn/ui](https://ui.shadcn.com)、Tailwind を利用し、Livewire スターター キットは Tailwind ベースの [Flux UI](https://fluxui.dev) コンポーネント ライブラリと Laravel Volt を利用します。

<!-- The React, Svelte, Vue, and Livewire starter kits all utilize Laravel's built-in authentication system to offer login, registration, password reset, email verification, and more. In addition, we are introducing a [WorkOS AuthKit-powered](https://authkit.com) variant of each starter kit, offering social authentication, passkeys, and SSO support. WorkOS offers free authentication for applications up to 1 million monthly active users. -->
React、Svelte、Vue、Livewire スターター キットはすべて、Laravel の組み込み認証システムを利用して、ログイン、登録、パスワードリセット、電子メール検証などを提供します。さらに、各スターター キットの [WorkOS AuthKit-powered](https://authkit.com) バリアントを導入し、ソーシャル認証、パスキー、SSO サポートを提供します。 WorkOS は、月間アクティブ ユーザー 100 万人までのアプリケーションに対して無料の認証を提供します。

<!-- With the introduction of our new application starter kits, Laravel Breeze and Laravel Jetstream will no longer receive additional updates. -->
新しいアプリケーションスターターキットの導入により、Laravel Breeze と Laravel Jetstream は追加のアップデートを受信しなくなります。

<!-- To get started with our new starter kits, check out the [starter kit documentation](/docs/12.x/starter-kits). -->
新しいスターター キットを使い始めるには、[starter kit documentation](/docs/12.x/starter-kits) をチェックしてください。

