// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99l.psi.Xbas99LTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xbas99l.psi.*;

public class Xbas99LSSubImpl extends ASTWrapperPsiElement implements Xbas99LSSub {

  public Xbas99LSSubImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99LVisitor visitor) {
    visitor.visitSSub(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99LVisitor) accept((Xbas99LVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<Xbas99LParam> getParamList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99LParam.class);
  }

  @Override
  @NotNull
  public Xbas99LSubprog getSubprog() {
    return findNotNullChildByClass(Xbas99LSubprog.class);
  }

}
