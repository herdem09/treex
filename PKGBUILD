# Maintainer: herdem09 herdem09@proton.me
pkgname=treex
pkgver=1.0.0
pkgrel=1
pkgdesc="TreeX - directory lister with color and summary features"
arch=('x86_64')
url="https://github.com/herdem09/treex"
license=('MIT')
depends=('python')
source=(
    "main.py"
    "README.md"
    "treex.conf"
)
sha256sums=('f28f0b5f7a5f151192cbafb66a3191da8362e169aa367d421ace839172741406'
            '7a4ea7a85f036a4d4c287c591f8d2276c19e7900665b980083ccd57e5827b839'
            '9879dc569d2a7197f59f5ef87b9a6bce21249d32604dfff35031960108046a42')

package() {
    mkdir -p "$pkgdir/usr/bin"
    cp main.py "$pkgdir/usr/bin/treex"
    chmod +x "$pkgdir/usr/bin/treex"

    mkdir -p "$pkgdir/etc/treex"
    cp treex.conf "$pkgdir/etc/treex/"
    
    mkdir -p "$pkgdir/usr/share/doc/treex"
    cp README.md "$pkgdir/usr/share/doc/treex/"
}
