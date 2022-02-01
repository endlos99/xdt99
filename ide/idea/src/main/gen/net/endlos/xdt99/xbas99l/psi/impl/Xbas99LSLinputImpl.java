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

public class Xbas99LSLinputImpl extends ASTWrapperPsiElement implements Xbas99LSLinput {

  public Xbas99LSLinputImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99LVisitor visitor) {
    visitor.visitSLinput(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99LVisitor) accept((Xbas99LVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<Xbas99LFStr> getFStrList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99LFStr.class);
  }

  @Override
  @Nullable
  public Xbas99LNexprn getNexprn() {
    return findChildByClass(Xbas99LNexprn.class);
  }

  @Override
  @Nullable
  public Xbas99LNvarW getNvarW() {
    return findChildByClass(Xbas99LNvarW.class);
  }

  @Override
  @NotNull
  public List<Xbas99LSexpr> getSexprList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99LSexpr.class);
  }

  @Override
  @NotNull
  public List<Xbas99LSvarR> getSvarRList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99LSvarR.class);
  }

  @Override
  @Nullable
  public Xbas99LSvarW getSvarW() {
    return findChildByClass(Xbas99LSvarW.class);
  }

}
