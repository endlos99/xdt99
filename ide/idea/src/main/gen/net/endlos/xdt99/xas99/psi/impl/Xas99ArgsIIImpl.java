// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99.psi.Xas99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99.psi.*;

public class Xas99ArgsIIImpl extends ASTWrapperPsiElement implements Xas99ArgsII {

  public Xas99ArgsIIImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99Visitor visitor) {
    visitor.visitArgsII(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99Visitor) accept((Xas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public Xas99Expr getExpr() {
    return findNotNullChildByClass(Xas99Expr.class);
  }

}
