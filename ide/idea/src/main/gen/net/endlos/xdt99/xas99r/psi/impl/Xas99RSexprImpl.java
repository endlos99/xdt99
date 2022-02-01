// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99r.psi.Xas99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99r.psi.*;

public class Xas99RSexprImpl extends ASTWrapperPsiElement implements Xas99RSexpr {

  public Xas99RSexprImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99RVisitor visitor) {
    visitor.visitSexpr(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99RVisitor) accept((Xas99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xas99ROpAddress getOpAddress() {
    return findChildByClass(Xas99ROpAddress.class);
  }

  @Override
  @Nullable
  public Xas99ROpLabel getOpLabel() {
    return findChildByClass(Xas99ROpLabel.class);
  }

  @Override
  @NotNull
  public List<Xas99RSexpr> getSexprList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xas99RSexpr.class);
  }

}
