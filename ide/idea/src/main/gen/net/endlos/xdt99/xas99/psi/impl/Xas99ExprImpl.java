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

public class Xas99ExprImpl extends ASTWrapperPsiElement implements Xas99Expr {

  public Xas99ExprImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99Visitor visitor) {
    visitor.visitExpr(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99Visitor) accept((Xas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<Xas99Expr> getExprList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xas99Expr.class);
  }

  @Override
  @Nullable
  public Xas99OpAddress getOpAddress() {
    return findChildByClass(Xas99OpAddress.class);
  }

  @Override
  @Nullable
  public Xas99OpLabel getOpLabel() {
    return findChildByClass(Xas99OpLabel.class);
  }

}
