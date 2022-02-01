// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99l.psi.Xbas99LTypes.*;
import net.endlos.xdt99.xbas99l.psi.*;
import com.intellij.navigation.ItemPresentation;
import com.intellij.psi.PsiReference;

public class Xbas99LNvarWImpl extends Xbas99LNamedElementImpl implements Xbas99LNvarW {

  public Xbas99LNvarWImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99LVisitor visitor) {
    visitor.visitNvarW(this);
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
  @NotNull
  public List<Xbas99LNexprn> getNexprnList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xbas99LNexprn.class);
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
  public @NotNull String getName() {
    return Xbas99LPsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xbas99LPsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xbas99LPsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public ItemPresentation getPresentation() {
    return Xbas99LPsiImplUtil.getPresentation(this);
  }

  @Override
  public PsiReference getReference() {
    return Xbas99LPsiImplUtil.getReference(this);
  }

}
