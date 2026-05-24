# リリースノート (Release Notes)

- [バージョン管理スキーム](#versioning-scheme)
- [サポートポリシー](#support-policy)
- [Laravel12](#laravel-12)

<a name="versioning-scheme"></a>
## バージョン管理スキーム (Versioning Scheme)

Laravel とその他のファーストパーティ パッケージは [セマンティック バージョニング](https://semver.org) に従います。メジャー フレームワーク リリースは毎年 (~第 1 四半期) リリースされますが、マイナー リリースとパッチ リリースは毎週リリースされる場合があります。マイナー リリースとパッチ リリースには重大な変更が含まれてはなりません**。

Laravel のメジャーリリースには重大な変更が含まれるため、アプリケーションまたはパッケージから Laravel フレームワークまたはそのコンポーネントを参照する場合は、必ず `^12.0` などのバージョン制約を使用する必要があります。ただし、私たちは常に 1 日以内に新しいメジャー リリースに更新できるように努めています。

<a name="named-arguments"></a>
#### 名前付き引数

[名前付き引数](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments) は、Laravel の下位互換性ガイドラインではカバーされていません。 Laravel コードベースを改善するために、必要に応じて関数の引数の名前を変更することもできます。したがって、Laravelメソッドを呼び出すときに名前付き引数を使用する場合は、パラメータ名が将来変更される可能性があることを理解した上で、慎重に行う必要があります。

<a name="support-policy"></a>
## サポートポリシー (Support Policy)

すべての Laravel リリースでは、バグ修正は 18 か月間提供され、セキュリティ修正は 2 年間提供されます。すべての追加ライブラリについては、最新のメジャー リリースのみがバグ修正を受けます。さらに、データベースのバージョン [Laravelによってサポートされています](/docs/{{version}}/database#introduction) を確認してください。

<div class="overflow-auto">

| バージョン | PHP(*)   | リリース             | バグ修正まで     | セキュリティ修正の期限 |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10      | 8.1～8.3 | 2023 年 2 月 14 日 | 2024 年 8 月 6 日    | 2025 年 2 月 4 日   |
| 11      | 8.2～8.4 | 2024 年 3 月 12 日    | 2025 年 9 月 3 日 | 2026 年 3 月 12 日     |
| 12      | 8.2～8.5 | 2025 年 2 月 24 日 | 2026 年 8 月 13 日   | 2027 年 2 月 24 日  |
| 13      | 8.3～8.5 | 2026 年第 1 四半期             | 2027 年第 3 四半期             | 2028 年第 1 四半期              |

</div>

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

(*) サポートされている PHP バージョン

<a name="laravel-12"></a>
## Laravel12 (Laravel 12)

Laravel 12 は、アップストリームの依存関係を更新し、ユーザー認証に [WorkOS認証キット](https://authkit.com) を使用するオプションを含む React、Svelte、Vue、Livewire の新しいスターター キットを導入することにより、Laravel 11.x で行われた改善を継続しています。スターター キットの WorkOS バリアントは、ソーシャル認証、パスキー、および SSO サポートを提供します。

<a name="minimal-breaking-changes"></a>
### 最小限の重大な変更

このリリース サイクルでは、重大な変更を最小限に抑えることに重点を置いています。その代わりに、私たちは既存のアプリケーションを壊すことなく、年間を通して継続的に生活の質を向上させることに専念してきました。

したがって、Laravel 12 リリースは、既存の依存関係をアップグレードするための比較的マイナーな「メンテナンス リリース」です。これを考慮すると、ほとんどの Laravel アプリケーションは、アプリケーション コードを変更せずに Laravel 12 にアップグレードできます。

<a name="new-application-starter-kits"></a>
### 新しいアプリケーション スターター キット

Laravel 12 では、React、Svelte、Vue、Livewire 用の新しい [アプリケーションスターターキット](/docs/{{version}}/starter-kits) が導入されています。 React、Svelte、Vue スターター キットは Inertia 2、TypeScript、[shadcn/ui](https://ui.shadcn.com)、Tailwind を利用し、Livewire スターター キットは Tailwind ベースの [フラックスUI](https://fluxui.dev) コンポーネント ライブラリと Laravel Volt を利用します。

React、Svelte、Vue、Livewire スターター キットはすべて、Laravel の組み込み認証システムを利用して、ログイン、登録、パスワードリセット、電子メール検証などを提供します。さらに、各スターター キットの [WorkOS AuthKit を利用した](https://authkit.com) バリアントを導入し、ソーシャル認証、パスキー、SSO サポートを提供します。 WorkOS は、月間アクティブ ユーザー 100 万人までのアプリケーションに対して無料の認証を提供します。

新しいアプリケーションスターターキットの導入により、Laravel Breeze と Laravel Jetstream は追加のアップデートを受信しなくなります。

新しいスターター キットを使い始めるには、[スターターキットのドキュメント](/docs/{{version}}/starter-kits) をチェックしてください。

